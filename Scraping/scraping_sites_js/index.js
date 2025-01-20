const { default: puppeteer } = require("puppeteer")
const csv = require('csv-parser')
const fs = require('fs')
const path = require('path')

const BASE_PATH = path.resolve('../site_data/')
console.log(BASE_PATH);

RESOLUTIONS = [
    {isMobile: false, resolution: {"width":  1536, "height": 864}},
    {isMobile: false, resolution: {"width":  1440, "height": 900}},
    {isMobile: false, resolution: {"width":  1366, "height": 768}},

    {isMobile: false, resolution: {"width":  1280, "height": 800}},
    {isMobile: true, resolution: {"width":  962, "height": 601}},
    {isMobile: true, resolution: {"width":  800, "height": 1280}},
    {isMobile: true, resolution: {"width":  810, "height": 1080}},

    {isMobile: true, resolution: {"width":  768, "height": 1024}},
    {isMobile: true, resolution: {"width":  600, "height": 962}},
    {isMobile: true, resolution: {"width":  480, "height": 800}},
    {isMobile: true, resolution: {"width":  414, "height": 736}},
]

async function screenshot(broswer, url) {

    let domain_name = url
    if (domain_name.includes('https://')) {
        domain_name = domain_name.substring(8)
    } else if (domain_name.includes('http://')) {
        domain_name = domain_name.substring(7)
    }

    if (domain_name.includes('www.')) {
        domain_name = domain_name.substring(4)
    }

    if (domain_name.includes('/')) {
        domain_name = domain_name.substring(0, domain_name.indexOf('/'))
    }

    const dir_name = `${BASE_PATH}/${domain_name}`
    if (!fs.existsSync(dir_name)) {
        fs.mkdirSync(dir_name)
    }

    const page = await broswer.newPage()
    await page.goto(url)
    await page.goto(url, {'waitUntil': 'domcontentloaded'})
    await new Promise(r => setTimeout(r, 2000));
    for (let i = 0; i < RESOLUTIONS.length; i++) {
        const {resolution, isMobile} =RESOLUTIONS[i];
        await page.setViewport({...resolution, isMobile})
        await page.screenshot({path: `${dir_name}/shot_${resolution.width}_${resolution.height}.png`, fullPage: true})
    }
    await page.close()
}

async function main() {
    const browser = await puppeteer.launch()
    await screenshot(browser, 'https://www.elpasocommercialappraisals.com/')
    await browser.close()
}

(async () => main())();