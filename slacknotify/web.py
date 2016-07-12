"""Function to connect"""
from io import BytesIO
from urllib.parse import urlencode
import logging
import ujson
import pycurl
from slacknotify.client import Client

def start_rtm(token):
    """Get WS URL"""
    fields = {
        "token": token
    }

    fields_encoded = urlencode(fields)
    url = 'https://slack.com/api/rtm.start'
    logging.info('Start: %s', url)
    logging.debug('Fields: %s', fields_encoded)

    buffer = BytesIO()
    curl = pycurl.Curl()
    curl.setopt(curl.URL, url)
    curl.setopt(curl.POSTFIELDS, fields_encoded)
    curl.setopt(curl.WRITEDATA, buffer)
    curl.perform()
    curl.close()

    response = ujson.decode(buffer.getvalue())
    logging.debug('Response: %s', response)
    return response

def connect_ws(response):
    """Connect with WS"""
    try:
        logging.info('WS Url: %s', response['url'])
        ws_client = Client(response)
        ws_client.connect()
        ws_client.run_forever()
    except KeyboardInterrupt:
        ws_client.close()
    finally:
        ws_client.close()
