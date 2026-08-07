#!/usr/bin/env python3
"""Capture un rollup HTML (800x2000px = 80x200cm) en haute résolution.

Usage: render_rollup.py <template.html> <visuel.png> <sortie.png> [scale]
"""
import sys
import base64
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

def data_uri(path: str, mime: str) -> str:
    b64 = base64.b64encode(Path(path).read_bytes()).decode()
    return f"data:{mime};base64,{b64}"

async def main():
    tmpl, visuel, out, scale = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]) if len(sys.argv) > 4 else 4.0
    base = Path(tmpl).resolve().parent

    html = Path(tmpl).read_text()
    # Injection base64 : logo, QR et visuel (évite les blocages file://)
    html = html.replace("file:///opt/data/prospecting_mairies/gumpy_logo.png",
                        data_uri(base / "gumpy_logo.png", "image/png"))
    html = html.replace("file:///opt/data/prospecting_mairies/gumpy_qr.png",
                        data_uri(base / "gumpy_qr.png", "image/png"))
    html = html.replace("__VISUEL__", data_uri(Path(visuel).resolve(), "image/png"))

    tmp = Path(tmpl).resolve().with_suffix(".tmp.html")
    tmp.write_text(html)

    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
        page = await browser.new_page(viewport={"width": 800, "height": 2000}, device_scale_factor=scale)
        await page.goto(tmp.as_uri())
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(500)
        await page.screenshot(path=out, full_page=True)
        await browser.close()

    tmp.unlink()
    w, h = 800 * scale, 2000 * scale
    print(f"OK {out}  {int(w)}x{int(h)}px")

asyncio.run(main())
