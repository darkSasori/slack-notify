"""WebSocket client"""
from subprocess import call
import logging
from ws4py.client.threadedclient import WebSocketClient
import ujson

class Client(WebSocketClient):
    """Websocket client implement"""
    def __init__(self, info):
        """Init class"""
        super(Client, self).__init__(info['url'])
        self.my_info = info['self']
        self.channels = {i['id']: i['name'] for i in info['channels']}
        self.groups = {i['id']: i['name'] for i in info['groups']}
        self.users = {i['id']: i['name'] for i in info['users']}
        logging.debug('Channels: %s', self.channels)
        logging.debug('Groups: %s', self.groups)
        logging.debug('Users: %s', self.users)

    def opened(self):
        logging.info('Connection opened')

    def received_message(self, recv):
        try:
            obj = ujson.decode(recv.data.decode('UTF-8'))
            logging.debug('Data: %s', obj)
            if obj['user'] == self.my_info['id']:
                return
            if obj['type'] == 'message':
                try:
                    channel = self.get_channel(obj['channel'])
                    msg = "%s: %s" % (channel, obj['text'])
                except KeyError:
                    user = self.get_user(obj['user'])
                    msg = "%s: %s" % (user, obj['text'])
                logging.debug('Call xcowsay with %s', msg)
                call(['xcowsay', msg])
        except KeyError as error:
            logging.warning('KeyError[%s]: %s', obj['type'], error)
            logging.debug('Data: %s', recv)

    def get_channel(self, code):
        """Get channel name"""
        try:
            return self.channels[code]
        except KeyError:
            return self.groups[code]
        return None

    def get_user(self, code):
        """Get user name"""
        try:
            return self.users[code]
        except KeyError:
            return None
