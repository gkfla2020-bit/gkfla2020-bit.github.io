import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 720})
        await page.goto(f'file:///Users/djajagggjg/gkfla2020-bit.github.io/esg-demo/ESG_TradeGuard_Presentation.pdf')
        await page.wait_for_timeout(3000)
        # PDF 뷰어에서 페이지 수 확인은 어려우니 파일 크기만
        import os
        size = os.path.getsize('ESG_TradeGuard_Presentation.pdf')
        print(f'PDF size: {size/1024/1024:.1f} MB')

        # 대신 PDF를 다시 열어서 첫 페이지 스크린샷
        await page.screenshot(path='verify_page1.png')
        print('Saved verify_page1.png')
        await browser.close()

asyncio.run(main())
