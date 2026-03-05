from playwright.async_api import async_playwright
import asyncio

class Scraper:
    """
    Handles scraping logic for cartoony.net.
    """
    @staticmethod
    async def fetch_episodes(season_id: int):
        """
        Scrapes a season page to extract episode IDs and names.
        """
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(f"https://cartoony.net/watch/{season_id}", wait_until="networkidle")
                await page.wait_for_timeout(2000)

                episodes = await page.evaluate("""() => {
                    const links = document.querySelectorAll('a[href*="/watch/"]');
                    const eps = [];
                    const seen = new Set();
                    for (const link of links) {
                        const match = link.href.match(/\\/watch\\/\\d+\\/(\\d+)/);
                        if (match) {
                            const id = parseInt(match[1]);
                            if (!seen.has(id)) {
                                seen.add(id);
                                const name = link.textContent.trim();
                                eps.push({ id, name });
                            }
                        }
                    }
                    return eps;
                }""")

                await browser.close()
                return episodes
        except Exception as e:
            raise e
