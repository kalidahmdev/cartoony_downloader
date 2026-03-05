from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import os
import sys

# Add src to the Python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")
sys.path.insert(0, os.path.join(BASE_DIR, "src"))

from engine import CartoonyDownloader
from utils import Scraper

app = FastAPI()

# Global reference to the active downloader
active_downloader = None

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open(os.path.join(STATIC_DIR, "index.html"), "r", encoding="utf-8") as f:
        return f.read()

@app.post("/cancel")
async def cancel_batch():
    global active_downloader
    if active_downloader:
        active_downloader.cancel()
        return JSONResponse({"status": "cancelled"})
    return JSONResponse({"status": "no_active_task"})

@app.get("/browse")
async def browse_folder():
    """Native folder picker using tkinter."""
    def _pick_folder():
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        folder = filedialog.askdirectory(title="Select Download Folder")
        root.destroy()
        return folder

    folder = await asyncio.to_thread(_pick_folder)
    return JSONResponse({"path": folder or ""})

@app.get("/fetch")
async def fetch_episodes(season_id: int):
    """Refactored to use the Scraper class."""
    try:
        episodes = await Scraper.fetch_episodes(season_id)
        return JSONResponse({"episodes": episodes})
    except Exception as e:
        return JSONResponse({"error": str(e), "episodes": []}, status_code=500)

@app.get("/run")
async def run_batch(season_id: int, episode_ids: str, tabs: int = 5, download_path: str = ""):
    """Streams automation logs via SSE."""
    global active_downloader
    ids = [int(x.strip()) for x in episode_ids.split(",") if x.strip()]

    async def log_generator():
        global active_downloader
        queue = asyncio.Queue()

        def sync_log_callback(msg):
            # Safe for both sync and async calls from engine
            asyncio.get_event_loop().call_soon_threadsafe(queue.put_nowait, msg)

        downloader = CartoonyDownloader(log_callback=sync_log_callback)
        active_downloader = downloader
        
        path = download_path if download_path else None
        # Start batch in background
        batch_task = asyncio.create_task(downloader.run_batch(season_id, ids, tabs, path))

        while True:
            try:
                # Use a small timeout to check if task is done
                msg = await asyncio.wait_for(queue.get(), timeout=1.0)
                yield f"data: {msg}\n\n"
            except asyncio.TimeoutError:
                if batch_task.done():
                    # Process any remaining messages in queue before finishing
                    while not queue.empty():
                        msg = queue.get_nowait()
                        yield f"data: {msg}\n\n"
                    break
        
        active_downloader = None
        yield "data: [DONE]\n\n"

    return StreamingResponse(log_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
