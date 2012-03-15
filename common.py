import mechanize
import os

class McGillException(Exception):
    pass

urls = {
    'login': 'twbkwbis.P_WWWLogin',
    'transcript': 'bzsktran.P_Display_Form?user_type=S&tran_type=V'
}
_base_url = 'https://banweb.mcgill.ca/pban1/%s'
urls = {k: _base_url % v for k,v in urls.items()}

browser = mechanize.Browser()

def login(sid=None, pin=None):
    if sid is None:
        sid = os.environ.get('MCGILL_SID', None)
    if pin is None:
        pin = os.environ.get('MCGILL_PIN', None)
    if sid is None or pin is None:
        raise McGillException('McGill ID or PIN not provided.')
    browser.open(urls['login'])
    browser.select_form('loginform')
    browser['sid'] = sid
    browser['PIN'] = pin
    response = browser.submit()
    if 'Authorization Failure' in response.read():
        raise McGillException('Invalid McGill ID or PIN.')
