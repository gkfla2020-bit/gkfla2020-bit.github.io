import asyncio
from playwright.async_api import async_playwright

URL = 'http://localhost:8080'

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 720})
        await page.goto(URL, wait_until='networkidle')
        await page.wait_for_timeout(3000)

        count = await page.evaluate('document.querySelectorAll(".ppt-slide").length')
        print(f'Total slides: {count}')

        # 각 슬라이드의 콘텐츠 높이 vs 뷰포트 높이 비교
        results = await page.evaluate('''() => {
            var slides = document.querySelectorAll('.ppt-slide');
            var results = [];
            slides.forEach((s, i) => {
                var c = s.firstElementChild;
                if (!c || c.classList.contains('slide-num')) {
                    c = s.children[0];
                }
                // 제목 텍스트 추출
                var title = '';
                var secTitle = s.querySelector('.sec-title');
                var stepTag = s.querySelector('.step-tag');
                if (secTitle) title = secTitle.textContent.trim();
                else if (stepTag) title = stepTag.textContent.trim();
                else {
                    var h1 = s.querySelector('h1');
                    if (h1) title = h1.textContent.trim();
                }

                var contentH = c ? c.scrollHeight : 0;
                var overflow = contentH > 720;
                results.push({
                    idx: i + 1,
                    title: title.substring(0, 40),
                    contentH: contentH,
                    overflow: overflow,
                    overflowPx: overflow ? contentH - 720 : 0
                });
            });
            return results;
        }''')

        print(f'\n{"#":>3} {"Title":<40} {"Height":>7} {"Status"}')
        print('-' * 70)
        for r in results:
            status = f'⚠ OVERFLOW +{r["overflowPx"]}px' if r['overflow'] else '✓ OK'
            print(f'{r["idx"]:>3} {r["title"]:<40} {r["contentH"]:>7} {status}')

        await browser.close()

asyncio.run(main())
