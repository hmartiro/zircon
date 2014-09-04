"""

"""

import time

from django.conf import settings

from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.sdjango import namespace

from zircon.datastores.influx import InfluxDatastore

NAMESPACE_URL = '/data'

@namespace(NAMESPACE_URL)
class DataNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):

    try:
        zircon_config = settings.ZIRCON_CONFIG
        db_info = zircon_config.get('db_info', None)
        db_name = zircon_config.get('db_name', None)
        db = InfluxDatastore(db_info=db_info, db_name=db_name)
    except AttributeError:
        print('[WARNING] No ZIRCON_CONFIG found in Django settings!')
        db = InfluxDatastore()

    def initialize(self):
        print('Socket.io session started on {}.'.format(NAMESPACE_URL))

    def log(self, channel, message):
        print("[{}] {} - {}".format(self.socket.sessid, channel, message))

    def on_debug(self, msg):
        self.log('DEBUG', msg)

    def db_api_wrapper(self, method_name, msg):
        arg = msg or {}
        try:
            return getattr(self.db, method_name)(**arg)
        except Exception, e:
            print(e)
            return None

    def on_time(self, msg):
        return int(time.time() * 1e6)

    def on_list_signals(self, msg):
        return self.db_api_wrapper('list_signals', msg)

    def on_get_database_name(self, msg):
        return self.db_api_wrapper('get_database_name', msg)

    def on_get_timeseries(self, msg):
        return self.db_api_wrapper('get_timeseries', msg)

    def on_get_last_points(self, msg):
        return self.db_api_wrapper('get_last_points', msg)


if __name__ == '__main__':

    # https://github.com/abourget/gevent-socketio/tree/master/examples/flask_chat
    pass
