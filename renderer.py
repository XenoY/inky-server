import sys
import asyncio
from pyppeteer import launch
import pathlib


async def render(html_path, png_path):
    html_path = pathlib.Path(html_path).resolve()  # Absoluter Pfad
    browser = await launch(executablePath="/usr/bin/chromium-browser", headless=True, args=["--no-sandbox"])
    page = await browser.newPage()
    await page.setViewport({"width": 1200, "height": 800})
    await page.goto(f"file://{html_path}", waitUntil="networkidle0")
    await page.screenshot({"path": png_path})
    await browser.close()

if __name__ == "__main__":
    html_path = sys.argv[1]
    png_path = sys.argv[2]
    asyncio.get_event_loop().run_until_complete(render(html_path, png_path))
