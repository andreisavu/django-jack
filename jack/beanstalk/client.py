
from django.conf import settings

from beanstalkc import Connection, CommandFailed

class Client(object):
    """ A simple proxy object over the default client """

    def __init__(self):
        self.conn = Connection(settings.BEANSTALK_HOST, settings.BEANSTALK_PORT)

    def __getattr__(self, name):
        return getattr(self.conn, name) 


