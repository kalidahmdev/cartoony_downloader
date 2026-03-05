import asyncio
import os
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from playwright_stealth import stealth_async
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration Defaults (can be overridden via .env)
DEFAULT_DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH", os.path.join(os.getcwd(), "downloads"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))
HEADLESS = os.getenv("HEADLESS", "False").lower() == "true"

class CartoonyDownloader:
    """
    Automates bulk video downloading from cartoony.net using Playwright.
    """
    def __init__(self, log_callback=None):
        self.log_callback = log_callback or print
        self.cancelled = False
        self.browser: Browser = None

    async def log(self, message: str):
        """Asynchronous log wrapper to support both sync and async callbacks."""
        if asyncio.iscoroutinefunction(self.log_callback):
            await self.log_callback(message)
        else:
            self.log_callback(message)

    def cancel(self):
        """Signals the downloader to stop all active tasks and close the browser."""
        self.cancelled = True
        if self.browser:
            asyncio.create_task(self._force_close())

    async def _force_close(self):
        """Immediate browser shutdown on cancellation."""
        try:
            if self.browser:
                await self.browser.close()
                await self.log("🛑 Browser force-closed due to cancellation.")
        except Exception:
            pass
        finally:
            self.browser = None

    async def click_play(self, page: Page, ep_id: int) -> bool:
        """
        Attempts to trigger video playback using 8 different strategies.
        Returns True if the 'data-paused' attribute is removed from the player.
        """
        strategies = [
            ("Playwright: Overlay Click", lambda: page.click("div.play-icon-overlay", timeout=5000)),
            ("Playwright: Button Click", lambda: page.click("button.play-icon-button", timeout=5000)),
            ("JS: Overlay element.click()", lambda: page.evaluate("document.querySelector('div.play-icon-overlay')?.click()")),
            ("JS: Button element.click()", lambda: page.evaluate("document.querySelector('button.play-icon-button')?.click()")),
            ("JS: PointerEvent Dispatch", lambda: page.evaluate("""() => {
                const el = document.querySelector('div.play-icon-overlay') || document.querySelector('button.play-icon-button');
                if (!el) return;
                ['pointerdown', 'pointerup', 'click'].forEach(type => {
                    el.dispatchEvent(new PointerEvent(type, {bubbles: true, cancelable: true, composed: true}));
                });
            }""")),
            ("API: Vidstack play()", lambda: page.evaluate("""() => {
                const player = document.querySelector('media-player');
                if (player && typeof player.play === 'function') player.play();
            }""")),
            ("Interaction: Media Play Button", lambda: page.evaluate("""() => {
                const btn = document.querySelector('media-play-button');
                if (btn) btn.click();
            }""")),
            ("Interaction: Bounding Box Center", lambda: self._click_player_center(page)),
        ]

        for i, (name, action) in enumerate(strategies):
            if self.cancelled:
                return False
            try:
                await self.log(f"EP {ep_id}: Strategy {i+1}/8: {name}")
                result = action()
                if asyncio.iscoroutine(result):
                    await result
                
                await page.wait_for_timeout(3000)

                # Verification check
                is_playing = await page.evaluate("""() => {
                    const player = document.querySelector('media-player');
                    return player && !player.hasAttribute('data-paused');
                }""")

                if is_playing:
                    await self.log(f"EP {ep_id}: ▶ Playback confirmed! ({name})")
                    return True
                else:
                    await self.log(f"EP {ep_id}: Strategy {i+1} failed to start playback.")
            except Exception as e:
                await self.log(f"EP {ep_id}: Strategy {i+1} error: {str(e)[:50]}...")

        return False

    async def _click_player_center(self, page: Page):
        """Utility to click the exact center of the media-player component."""
        box = await page.locator("media-player").first.bounding_box()
        if box:
            await page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)

    async def _poll_progress(self, page: Page, ep_id: int):
        """Polls the UI for assembly progress messages and logs updates."""
        last_pct = -1
        while not self.cancelled:
            try:
                progress = await page.evaluate("""() => {
                    const allText = document.body.innerText;
                    const match = allText.match(/(\\d{1,3})\\s*%/);
                    if (match) return parseInt(match[1]);
                    
                    const bar = document.querySelector('.progress-bar, progress');
                    if (bar) {
                        const w = bar.style?.width;
                        if (w && w.endsWith('%')) return parseInt(w);
                        if (bar.value !== undefined && bar.max) return Math.round((bar.value / bar.max) * 100);
                    }
                    return -1;
                }""")
                if progress >= 0 and progress != last_pct:
                    await self.log(f"EP {ep_id}: 📊 Progress: {progress}%")
                    last_pct = progress
                if progress >= 100:
                    break
            except Exception:
                break
            await asyncio.sleep(3)

    async def download_episode(self, context: BrowserContext, season_id: int, ep_id: int, download_path: str) -> bool:
        """Handles the end-to-end automation for a single episode tab."""
        if self.cancelled:
            return False

        url = f"https://cartoony.net/watch/{season_id}/{ep_id}"
        page = await context.new_page()
        await stealth_async(page)

        try:
            await self.log(f"🔄 EP {ep_id}: Loading automation...")
            await page.goto(url, wait_until="networkidle", timeout=60000)
            await page.wait_for_timeout(2000)

            if self.cancelled: return False

            # Phase 1: Playback
            played = await self.click_play(page, ep_id)
            if not played:
                await self.log(f"❌ EP {ep_id}: All play strategies exhausted.")
                return False

            if self.cancelled: return False

            # Phase 2: Download Button Activation
            await self.log(f"EP {ep_id}: Waiting for Download activation...")
            try:
                await page.wait_for_function("""() => {
                    const btn = document.querySelector('button.download-button');
                    if (!btn) return false;
                    const style = window.getComputedStyle(btn);
                    return style.opacity !== '0.5' && style.opacity !== '0' && style.display !== 'none';
                }""", timeout=45000)
            except Exception:
                await self.log(f"EP {ep_id}: Timed out waiting for button activation, attempting click...")

            # Phase 3: Selection & Quality
            await page.locator("button.download-button").click()
            await page.wait_for_timeout(3000)
            
            # Select 1080p if possible, else 720p
            quality_priorities = ["1920x1080", "1280x720"]
            quality_btn = None

            for q in quality_priorities:
                btn = page.locator(f"text={q}").first
                try:
                    await btn.wait_for(state="visible", timeout=3000)
                    quality_btn = btn
                    await self.log(f"EP {ep_id}: Quality selected ({q})")
                    break
                except Exception:
                    continue
            
            if not quality_btn:
                await self.log(f"❌ EP {ep_id}: Quality selector not found.")
                return False

            # Phase 4: Download Stream
            await self.log(f"EP {ep_id}: ⏳ High-speed segment assembly started...")
            progress_task = asyncio.create_task(self._poll_progress(page, ep_id))

            try:
                async with page.expect_download(timeout=0) as download_info:
                    await quality_btn.click()

                progress_task.cancel()
                download = await download_info.value
                file_name = download.suggested_filename
                os.makedirs(download_path, exist_ok=True)
                output_path = os.path.join(download_path, file_name)

                await self.log(f"EP {ep_id}: 💾 Saving File: {file_name}")
                await download.save_as(output_path)
                await self.log(f"✅ EP {ep_id}: Download Complete!")
                return True

            except Exception as e:
                progress_task.cancel()
                raise e

        except Exception as e:
            if not self.cancelled:
                await self.log(f"❌ EP {ep_id}: Fatal Error - {str(e)[:100]}")
            return False
        finally:
            await page.close()

    async def run_batch(self, season_id: int, episode_ids: list, tabs: int = 5, download_path: str = None):
        """Main entry point for batch processing with auto-retry logic."""
        download_path = download_path or DEFAULT_DOWNLOAD_PATH
        all_ids = list(episode_ids)
        total = len(all_ids)
        
        await self.log(f"📦 Starting Batch: {total} items | {tabs} Threads")
        await self.log(f"📂 Destination: {download_path}")

        failed_ids = []

        try:
            async with async_playwright() as p:
                self.browser = await p.chromium.launch(headless=HEADLESS)
                context = await self.browser.new_context(accept_downloads=True)

                # Main Processing Loop
                for i in range(0, total, tabs):
                    if self.cancelled: break
                    chunk = all_ids[i : i + tabs]
                    await self.log(f"🚀 Round Start: Processing {chunk}")

                    tasks = [self.download_episode(context, season_id, ep_id, download_path) for ep_id in chunk]
                    results = await asyncio.gather(*tasks, return_exceptions=True)

                    for ep_id, result in zip(chunk, results):
                        if isinstance(result, Exception) or not result:
                            if not self.cancelled:
                                await self.log(f"⚠️ EP {ep_id}: Round Failed.")
                                failed_ids.append(ep_id)

                # Auto-Retry Mechanism
                retry_round = 0
                while failed_ids and retry_round < MAX_RETRIES and not self.cancelled:
                    retry_round += 1
                    retry_list = list(failed_ids)
                    failed_ids.clear()
                    await self.log(f"🔁 Retry Round {retry_round}/{MAX_RETRIES} for {len(retry_list)} items.")

                    for i in range(0, len(retry_list), tabs):
                        if self.cancelled: break
                        chunk = retry_list[i : i + tabs]
                        tasks = [self.download_episode(context, season_id, ep_id, download_path) for ep_id in chunk]
                        results = await asyncio.gather(*tasks, return_exceptions=True)

                        for ep_id, result in zip(chunk, results):
                            if isinstance(result, Exception) or not result:
                                if not self.cancelled:
                                    failed_ids.append(ep_id)

                await self.browser.close()
                self.browser = None

        except Exception as e:
            if not self.cancelled:
                await self.log(f"❌ Fatal Engine Error: {str(e)}")

        if self.cancelled:
            await self.log("🛑 Automation terminated by user.")
        elif failed_ids:
            await self.log(f"⚠️ Batch finished with {len(failed_ids)} failures: {failed_ids}")
        else:
            await self.log("🎉 All downloads finished successfully!")
