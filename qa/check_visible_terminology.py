"""Require essential vocabulary on its teaching slide and exported PDF page.

The recording transcript and hidden course data do not satisfy this check.
Requires a running preview, Playwright, Chromium, and pdftotext.
"""
import asyncio
import json
import os
from pathlib import Path
import re
import subprocess

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get('COURSE_BASE_URL', 'http://127.0.0.1:8877').rstrip('/')


def normalized(text):
    # PDF text extraction can wrap a hyphenated term between its two words.
    text = re.sub(r'(?<=[-–—])\s*\n\s*', '', text).replace('\u00ad', '')
    return re.sub(r'\s+', ' ', text).strip().casefold()


async def main():
    terms = json.loads((ROOT/'qa/essential-terms.json').read_text())
    course = json.loads((ROOT/'course.json').read_text())
    slides = {s['id']: (c, s) for c in course for s in c['slides']}
    errors = []
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        page = await browser.new_page(reduced_motion='reduce')
        page.on('pageerror', lambda error: errors.append(str(error)))
        await page.goto(BASE+'/index.html')
        for width in [320, 1440]:
            await page.set_viewport_size({'width': width, 'height': 1000})
            for key, expected in terms.items():
                chapter, slide = slides[key]
                number = key.split('s')[1].lstrip('0')
                await page.evaluate('(hash)=>location.hash=hash', f"chapter-{chapter['number']}-slide-{number}")
                label = f"Chapter {chapter['number']}, {slide['stage']}"
                await page.wait_for_function('(label)=>document.querySelector("#app .slide")?.getAttribute("aria-label")===label', arg=label)
                text = normalized(await page.locator('#app .slide .slide-copy').inner_text())
                for term in expected:
                    assert normalized(term) in text, (width, key, term, 'missing from visible teaching slide')
                assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'), (width, key, 'horizontal overflow')
                if key == 'c01s04b':
                    assert await page.locator('#app .slide strong').filter(has_text='Fundamental attribution error').count() == 1
                    if width == 1440:
                        await page.locator('#app .slide').screenshot(path=str(ROOT/'out/terminology-desktop.png'))
        await browser.close()
    assert not errors, errors
    for key, expected in terms.items():
        chapter, slide = slides[key]
        slide_number = chapter['slides'].index(slide)+1
        page_number = sum(len(c['slides']) for c in course if c['number'] < chapter['number'])+slide_number
        files = [(ROOT/'common-ground-slides.pdf', page_number),
                 (ROOT/f"chapters/chapter-{chapter['number']:02d}.pdf", slide_number)]
        for path, number in files:
            text = normalized(subprocess.check_output(['pdftotext', '-f', str(number), '-l', str(number), str(path), '-'], text=True))
            for term in expected:
                assert normalized(term) in text, (str(path), number, term, 'missing from PDF teaching slide')
    result = dict(revision='visible-terminology', teaching_slides=len(terms), term_appearances=sum(map(len, terms.values())),
                  widths=[320, 1440], transcript_excluded=True, visible_bold_term='passed',
                  complete_and_chapter_pdf_terms='passed', js_errors=errors)
    (ROOT/'qa/visible-terminology-results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    asyncio.run(main())
