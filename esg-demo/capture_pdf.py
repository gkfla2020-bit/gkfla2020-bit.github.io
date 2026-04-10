import asyncio
from playwright.async_api import async_playwright

URL = 'http://localhost:8080'

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        # 브라우저 뷰포트를 16:9로
        page = await browser.new_page(viewport={'width': 1280, 'height': 720})
        await page.goto(URL, wait_until='networkidle')
        # JS fitSlides 실행 대기
        await page.wait_for_timeout(3000)

        # 슬라이드 번호만 숨기기 (나머지는 HTML 그대로)
        await page.evaluate('''() => {
            document.querySelectorAll('.slide-num').forEach(e => e.style.display='none');
        }''')

        count = await page.evaluate('document.querySelectorAll(".ppt-slide").length')
        print(f'{count} slides, printing PDF...')

        await page.pdf(
            path='ESG_TradeGuard_Presentation.pdf',
            width='1280px',
            height='720px',
            margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'},
            print_background=True,
            prefer_css_page_size=True,
        )

        await browser.close()
        print(f'Done: ESG_TradeGuard_Presentation.pdf')

asyncio.run(main())
