
from django.conf import settings

from beanstalkc import Connection, CommandFailed
from beanstalkc import SocketError as ConnectionError

class Client(object):
    """ A simple proxy object over the default client """

    def __init__(self, request):
        if hasattr(request, 'connection'):
            self.conn = Connection(request.connection[0], request.connection[1])
        elif settings.BEANSTALK_SERVERS:
            server = settings.BEANSTALK_SERVERS[0]
            self.conn = Connection(server[0], server[1])
        else:
            raise Exception("No servers defined.")

    def __getattr__(self, name):
        return getattr(self.conn, name) 


