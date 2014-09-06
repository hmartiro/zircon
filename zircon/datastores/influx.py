"""

"""

import time
from influxdb import client as influxdb

from zircon.datastores.base import BaseDatastore


class InfluxDatastore(BaseDatastore):

    # Try default database configuration if none provided
    DEFAULT_DB_INFO = {
        'host': 'localhost',
        'port': 8086,
        'username': 'root',
        'password': 'root'
    }

    DEFAULT_DB_NAME = 'zircon'

    def __init__(self, db_info=None, db_name=None):

        self.db_info = db_info or self.DEFAULT_DB_INFO
        self.db_name = db_name or self.DEFAULT_DB_NAME

        self.db = influxdb.InfluxDBClient(
            host=self.db_info['host'],
            port=self.db_info['port'],
            username=self.db_info['username'],
            password=self.db_info['password']
        )

        if self.db_name not in self.list_databases():
            self.create_database(self.db_name)

        self.switch_database(self.db_name)

        print('Using InfluxDB datastore with db name {}'.format(self.db_name))

    def create_database(self, db_name):
        self.db.create_database(db_name)

    def delete_database(self, db_name):
        self.db.delete_database(db_name)

    def switch_database(self, db_name):
        self.db_name = db_name
        self.db.switch_db(db_name)
        return True

    def get_database_name(self):
        return self.db_name

    def list_databases(self):
        return [d['name'] for d in self.db.get_database_list()]

    def list_signals(self):

        r = self.db.query('list series')

        try:
            return [s[1] for s in r[0]['points']]
        except(IndexError, KeyError):
            return None

    def delete_signal(self, signal_name):
        self.db.delete_series(signal_name)

    def write_points(self, data):

        return self.db.write_points_with_precision(data, time_precision='u')

    def query(self, query):

        print('[QUERY] {}'.format(query))
        return self.db.query(query, time_precision='u')

    def insert(self, data):

        # print('[INSERTED] {}'.format(data))

        insert_data = [{
            'name': signal_name,
            'columns': ['time', 'val'],
            'points': points
        } for signal_name, points in data.items()]

        now = time.time()

        result = self.write_points(insert_data)

        if not result:
            return False

        for signal in data:
            print('[{}] Saved {} points'.format(
                signal,
                len(data[signal])
            ))

        print('Saved total {} points in {} ms, success: {}'.format(
            sum([len(s) for s in data.values()]),
            (time.time() - now) * 1000,
            result
        ))

        return True

    def get_last_points(self, signals, num=1):

        all_signals = self.list_signals()
        query_signals = [s for s in signals if s in all_signals]

        if not query_signals:
            return {}

        query_str = 'select * from {} limit {}'.format(
            ', '.join(['{}'.format(s) for s in query_signals]),
            num
        )

        r = self.query(query_str)

        try:
            return {r_s['name']: [[p[0], p[2]]
                                  for p in r_s['points']] for r_s in r}
        except Exception, e:
            print(e)
            return None

    def get_timeseries(self, signals, t0, t1,
                       dt=100000, aggregate='last', limit=1000):

        all_signals = self.list_signals()
        query_signals = [s for s in signals if s in all_signals]

        if not query_signals:
            return {}

        q = 'select {}(val) from {} where time > {}u and time < {}u ' \
            'group by time({}u) limit {}'.format(
                aggregate,
                ', '.join(query_signals),
                int(t0),
                int(t1),
                int(dt),
                int(limit)
            )

        r = self.query(q)

        try:
            return {r_s['name']: r_s['points'] for r_s in r}
        except Exception, e:
            print(e)
            return None
