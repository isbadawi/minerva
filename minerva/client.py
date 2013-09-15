import os

import requests

from . import transcript


class error(Exception):
    pass

urls = {
    'login': 'twbkwbis.P_ValLogin',
    'transcript': 'bzsktran.P_Display_Form?user_type=S&tran_type=V'
}
_base_url = 'https://horizon.mcgill.ca/pban1/%s'
urls = {k: _base_url % v for k, v in urls.items()}


class MinervaClient(object):
    def __init__(self, sid):
        self.sid = sid
        self.session = requests.Session()

    def __repr__(self):
        return '<MinervaClient: %s>' % self.sid

    def login(self, pin):
        data = {'sid': self.sid, 'PIN': pin}
        cookies = {'TESTID': 'set'}
        response = self.session.post(urls['login'], data=data, cookies=cookies)
        return 'Authorization Failure' not in response.text

    def transcript(self):
        raw_transcript = self.session.get(urls['transcript']).text
        return transcript.scrape(raw_transcript)


def login(sid=None, pin=None):
    if sid is None:
        sid = os.environ.get('MINERVA_USER', None)
    if pin is None:
        pin = os.environ.get('MINERVA_PASS', None)
    if sid is None or pin is None:
        raise error('McGill ID or PIN not provided.')
    client = MinervaClient(sid)
    if not client.login(pin):
        raise error('Invalid McGill ID or PIN.')
    return client
