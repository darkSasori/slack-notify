import ujson
import logging
from ws4py.client.threadedclient import WebSocketClient
from subprocess import call

class Client(WebSocketClient):
    def set_info(self, info):
        self.me = info['self']
        self.channels = {i['id']: i['name'] for i in info['channels']}
        self.groups = {i['id']: i['name'] for i in info['groups']}
        self.users = {i['id']: i['name'] for i in info['users']}
        logging.debug('Channels: %s' % self.channels)
        logging.debug('Groups: %s' % self.groups)
        logging.debug('Users: %s' % self.users)

    def opened(self):
        logging.info('Connection opened')

    def received_message(self, recv):
        try:
            obj = ujson.decode(recv.data.decode('UTF-8'))
            logging.debug('Data: %s' % obj)
            if obj['user'] == self.me['id']:
                return
            if obj['type'] == 'message':
                try:
                    channel = self.get_channel(obj['channel'])
                    msg = "%s: %s" % (channel, obj['text'])
                except:
                    user = self.get_user(obj['user'])
                    msg = "%s: %s" % (user, obj['text'])
                logging.debug('Call xcowsay with %s' % msg)
                call(['xcowsay', msg])
        except Exception as err:
            logging.warning('Error[%s]: %s' % (obj['type'], err))
            logging.debug('Data: %s' % recv)

    def closed(self, reason, msg):
        logging.info("Closed[%d]: %s" %(reason, msg))

    def get_channel(self, id):
        try:
            return self.channels[id]
        except:
            return self.groups[id]
        return None

    def get_user(self, id):
        try:
            return self.users[id]
        except:
            return None
