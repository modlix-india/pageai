import asyncio
from pyppeteer import launch
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from os import path, mkdir

RESOLUTIONS = [
    # Desktop Resolutions
    # {"width":  2560, "height": 1600},
    # {"width":  1920, "height": 1080},
    # {"width":  1600, "height": 900},
    {"width":  1536, "height": 864},
    {"width":  1440, "height": 900},
    {"width":  1366, "height": 768},

    # Tablet Resolutions
    {"width":  1280, "height": 800},
    {"width":  962, "height": 601},
    {"width":  800, "height": 1280},
    {"width":  810, "height": 1080},

    # Mobile Resolutions
    {"width":  768, "height": 1024},
    {"width":  600, "height": 962},
    {"width":  480, "height": 800},
    {"width":  414, "height": 736},
]


async def screenshot(browser, url):
    if len(url.strip()) == 0:
        return

    page = await browser.newPage()

    print('Processing : ' + url)

    domain_name = url
    if (domain_name.index('https://') == 0):
        domain_name = domain_name[8:]
    elif (domain_name.index('http://') == 0):
        domain_name = domain_name[7:]

    if (domain_name.index('www.') == 0):
        domain_name = domain_name[4:]

    if (domain_name.index('/') > 0):
        domain_name = domain_name[:domain_name.index('/')]

    await page.goto(url, {'waitUntil': 'domcontentloaded'})
    await page.waitFor(4000)

    if not path.exists('screenshots/' + domain_name):
        mkdir('screenshots/' + domain_name)

    for resolution in RESOLUTIONS:
        await page.setViewport(resolution)
        await page.waitFor(2000)
        await page.screenshot({'path': 'screenshots/' + domain_name + '/' + str(resolution['width']) + 'x' + str(resolution['height']) + '.png', 'fullPage': True})

    await page.close()


async def thread(i, urls):
    browser = await launch(headless=True, executablePath='/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary')
    for url in urls:
        await screenshot(browser, url)
    await browser.close()
    return i


def wrapper(urls):
    return asyncio.run(thread(0, urls))


# not a good idea to run coroutines in another thread
if __name__ == "__main__":

    urls = pd.read_csv('site_list/jasminedirectory.csv', header=None)

    with ProcessPoolExecutor(max_workers=10) as pool:
        urls = urls[0].tolist()
        futs = []

        pool.map(wrapper, map(lambda x: urls[x:x+10], range(0, len(urls), 10)))

        # for i in range(0, len(urls), 10):
        # pool.apply_async
        # loop.run_until_complete(thread(i, urls[i:i+10]))
        #     futs.append(loop.run_in_executor(
        #         pool, wrapper, thread(i, urls[i:i+10])))
        # asyncio.gather(*futs)
