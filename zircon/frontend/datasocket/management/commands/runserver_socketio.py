"""

"""

from re import match
from os import environ

from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler
from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands.runserver import naiveip_re, DEFAULT_PORT
from django.utils import autoreload

from socketio.server import SocketIOServer


class Command(BaseCommand):

    def handle(self, *args, **options):

        autoreload.main(self.start_server, args, options)

    def start_server(self, addrport="", *args, **options):

        if not addrport:
            self.addr = '127.0.0.1'
            self.port = DEFAULT_PORT
        else:
            m = match(naiveip_re, addrport)
            if m is None:
                raise CommandError('"%s" is not a valid port number '
                                   'or address:port pair.' % addrport)
            self.addr, _, _, _, self.port = m.groups()

        # Make the port available here for the path:
        # socketio_tags.socketio ->
        # socketio_scripts.html ->
        # io.Socket JS constructor
        # allowing the port to be set as the client-side default there.
        environ["DJANGO_SOCKETIO_PORT"] = str(self.port)

        bind = (self.addr, int(self.port))
        print
        print "SocketIOServer running on http://%s:%s" % bind
        print
        handler = self.get_handler(*args, **options)
        server = SocketIOServer(bind, handler, resource="zircon",
                                policy_server=True)
        server.serve_forever()

    @staticmethod
    def get_handler(*args, **options):
        """
        Returns the django.contrib.staticfiles handler.
        """
        handler = WSGIHandler()
        try:
            from django.contrib.staticfiles.handlers import StaticFilesHandler
        except ImportError:
            return handler
        use_static_handler = options.get('use_static_handler', True)
        insecure_serving = options.get('insecure_serving', False)
        if (settings.DEBUG and use_static_handler or
                (use_static_handler and insecure_serving)):
            handler = StaticFilesHandler(handler)
        return handler
