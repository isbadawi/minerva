import mechanize
import os

from transcript import Transcript

class error(Exception):
    pass

urls = {
    'login': 'twbkwbis.P_WWWLogin',
    'transcript': 'bzsktran.P_Display_Form?user_type=S&tran_type=V'
}
_base_url = 'https://horizon.mcgill.ca/pban1/%s'
urls = {k: _base_url % v for k,v in urls.items()}

class McGillClient(object):
    def __init__(self, sid, browser):
        self.sid = sid
        self.browser = browser

    def __repr__(self):
        return '<McGillClient: %s>' % self.sid

    @property
    def transcript(self):
        raw_transcript = self.browser.open(urls['transcript'])
        return Transcript.from_html(raw_transcript)

def login(sid=None, pin=None):
    if sid is None:
        sid = os.environ.get('MCGILL_SID', None)
    if pin is None:
        pin = os.environ.get('MCGILL_PIN', None)
    if sid is None or pin is None:
        raise error('McGill ID or PIN not provided.')
    browser = mechanize.Browser()
    browser.open(urls['login'])
    browser.select_form('loginform')
    browser['sid'] = sid
    browser['PIN'] = pin
    response = browser.submit()
    if 'Authorization Failure' in response.read():
        raise error('Invalid McGill ID or PIN.')
    return McGillClient(sid, browser)
