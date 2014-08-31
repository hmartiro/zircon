"""

"""

from abc import ABCMeta, abstractmethod


class BaseDatastore():
    """ Abstract base class defining the Datastore interface.

    A Datastore is a connector to something that can store timeseries data.
    It provides an interface to add, remove, and access timeseries data
    efficiently. A single piece of information consists of a signal name,
    a timestamp in microseconds, and some associated data.

    To be efficient, a Datastore should keep information sorted by timestamp
    and separated by signal name. The most important ingredient is that the
    most recent N points for a given signal can be retrieved in constant time.

    What kind of data can be stored depends on the implementation. For
    example, a Datastore may accept integers, floats, strings, or any
    combination.

    **Usage**::

        datastore = Datastore()

        print(datastore.list_signals())

        signal = datastore.get_last_points('MY_SIGNAL', 10)

        datastore.insert({'MY_SIGNAL': [[12345, -5.2], [12346, 2.1]]})
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def create_database(self, db_name):
        """ Create a database.
        """
        raise NotImplementedError()

    @abstractmethod
    def delete_database(self, db_name):
        """ Delete a database.
        """
        raise NotImplementedError()

    @abstractmethod
    def switch_database(self, db_name):
        """ Switch the current database.
        """
        raise NotImplementedError()

    @abstractmethod
    def list_databases(self):
        """ Return a list of databases.
        """
        raise NotImplementedError()

    @abstractmethod
    def list_signals(self):
        """ Return a list of signals in this database.
        """
        raise NotImplementedError()

    @abstractmethod
    def delete_signal(self, data):
        """ Delete this signal and all associated data.
        """
        raise NotImplementedError()

    @abstractmethod
    def insert(self, data):
        """ Add data to the database.

        :param data: Dictionary mapping signal names to timeseries.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_last_points(self, signals, num):
        """ Get the last N points for the given signals.
        :param signals:
        :param num:
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def get_timeseries(self, signals, t0, t1, dt, aggregate, limit):
        raise NotImplementedError()
