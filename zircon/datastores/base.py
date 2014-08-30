"""

"""

from abc import ABCMeta, abstractmethod


class BaseDatastore():

    __metaclass__ = ABCMeta

    @abstractmethod
    def create_database(self, db_name):
        raise NotImplementedError()

    @abstractmethod
    def delete_database(self, db_name):
        raise NotImplementedError()

    @abstractmethod
    def switch_database(self, db_name):
        raise NotImplementedError()

    @abstractmethod
    def list_databases(self):
        raise NotImplementedError()

    @abstractmethod
    def list_signals(self, data):
        raise NotImplementedError()

    @abstractmethod
    def delete_signal(self, data):
        raise NotImplementedError()

    @abstractmethod
    def insert(self, data):
        raise NotImplementedError()

    @abstractmethod
    def get_last_points(self, signals, num):
        raise NotImplementedError()

    @abstractmethod
    def get_timeseries(self, signals, t0, t1, dt, aggregate, limit):
        raise NotImplementedError()
