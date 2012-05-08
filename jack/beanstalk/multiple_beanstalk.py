from django.conf import settings

class Middleware(object):
    def process_request(self, request):
        if 'conn' not in request.COOKIES:
            return

        conn_id = int(request.COOKIES['conn'])
        request.connection = settings.BEANSTALK_SERVERS[conn_id]

def ContextProcessor(request):
    if 'conn' not in request.COOKIES:
        conn_id = None
    else:
        conn_id = int(request.COOKIES['conn'])
    return {'connections':settings.BEANSTALK_SERVERS,'conn_id':conn_id}

