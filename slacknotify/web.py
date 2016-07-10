import ujson
import pycurl
from io import BytesIO
from urllib.parse import urlencode
from slacknotify.client import Client
import logging

def start_rtm(token):
    fields = {
        "token": token
    }

    fields_encoded = urlencode(fields)
    url = 'https://slack.com/api/rtm.start'
    logging.info('Start: %s' % url)
    logging.debug('Fields: %s' % fields_encoded)

    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.POSTFIELDS, fields_encoded)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    response = ujson.decode(buffer.getvalue())
    logging.debug('Response: %s' % response)
    return response

def connect_ws(response):
    try:
        logging.info('WS Url: %s' % response['url'])
        ws = Client(response['url'])
        ws.set_info(response)
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
    except Exception as err:
        print("Error: %s" % err)
    finally:
        ws.close()
