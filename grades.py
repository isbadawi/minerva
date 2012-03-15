from common import browser, urls

def _build_transcript():
    response = browser.open(urls['transcript'])
    return response
