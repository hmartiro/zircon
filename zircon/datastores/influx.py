"""

"""

from zircon.datastores.base import BaseDatastore


class InfluxDatastore(BaseDatastore):

    def __init__(self):
        self.callback = None

    def create_database(self, db_name):
        return True

    def delete_database(self, db_name):
        return True

    def switch_database(self, db_name):
        return True

    def list_databases(self):
        return []

    def list_signals(self, data):
        return []

    def delete_signal(self, data):
        return True

    def insert(self, data):
        print('[INSERTED] {}'.format(data))
        return True

    def get_last_points(self, signals, num):
        return {}

    def get_timeseries(self, signals, t0, t1, dt, aggregate, limit):
        return {}
