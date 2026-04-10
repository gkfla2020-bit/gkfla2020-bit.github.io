import asyncio
from playwright.async_api import async_playwright

URL = 'http://localhost:8080'

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 720})
        await page.goto(URL, wait_until='networkidle')
        await page.wait_for_timeout(3000)

        # 기존 scale 제거 후 측정
        results = await page.evaluate('''() => {
            document.querySelectorAll('.ppt-slide').forEach(s => {
                var c = s.firstElementChild;
                if (c && !c.classList.contains('slide-num')) {
                    c.style.transform = 'none';
                    c.style.width = '';
                    c.style.marginLeft = '';
                }
            });

            var slides = document.querySelectorAll('.ppt-slide');
            var results = [];
            slides.forEach((s, i) => {
                var c = s.firstElementChild;
                if (!c || c.classList.contains('slide-num')) {
                    results.push({idx: i+1, h: 0, scale: 1, ok: true});
                    return;
                }
                var h = c.scrollHeight;
                var overflow = h > 720;
                var scale = overflow ? 700 / h : 1;
                if (overflow) {
                    c.style.transform = 'scale(' + scale + ')';
                    c.style.transformOrigin = 'top center';
                }
                results.push({idx: i+1, h: h, scale: parseFloat(scale.toFixed(3)), ok: !overflow, after: overflow ? Math.round(h * scale) : h});
            });
            return results;
        }''')

        print(f'{"#":>3} {"Original":>8} {"Scale":>7} {"After":>7} {"Status"}')
        print('-' * 45)
        for r in results:
            status = '✓' if r['ok'] else f'→ scale({r["scale"]})'
            print(f'{r["idx"]:>3} {r["h"]:>8}px {r["scale"]:>7} {r.get("after",r["h"]):>6}px {status}')

        await browser.close()

asyncio.run(main())
