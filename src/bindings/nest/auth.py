import requests
import json
import datetime
from cfg import date_format
from log.log import log_error


def get_accesstoken(client_id, client_secret, pincode):
    url_access = 'https://api.home.nest.com/oauth2/access_token'
    #
    headers = {'Connection': 'close',
               'User-Agent': 'Linux/2.6.18 UDAP/2.0 CentOS/5.8',
               'Content-type': 'application/x-www-form-urlencoded'}
    #
    payload = {'client_id': client_id,
               'client_secret': client_secret,
               'code': pincode,
               'grant_type': 'authorization_code'}
    #
    r = requests.post(url_access,
                      headers=headers,
                      data=payload)
    #
    if r.status_code != requests.codes.ok:
        log_error('Access Token not returned by Nest server')
        raise Exception()
    #
    try:
        response = json.loads(r.text)
    except Exception as e:
        log_error('Access Token not returned by Nest server .')
        raise Exception()
    #
    token = response['access_token']
    tokenexpiry = (datetime.datetime.now() + datetime.timedelta(seconds=response['expires_in'])).strftime(date_format)
    #
    return {'token': token,
            'tokenexpiry': tokenexpiry}
