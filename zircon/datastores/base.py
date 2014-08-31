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
    combination of them.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def create_database(self, db_name):
        """ Create a database.

        :returns: True if successful, False otherwise.
        """
        raise NotImplementedError()

    @abstractmethod
    def delete_database(self, db_name):
        """ Delete a database.

        :returns: True if successful, False otherwise.
        """
        raise NotImplementedError()

    @abstractmethod
    def switch_database(self, db_name):
        """ Switch the current database.

        :returns: True if successful, False otherwise.
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

        >>> datastore.list_signals()
        ['SIGNAL_A', 'SIGNAL_B', 'SIGNAL_C']
        """
        raise NotImplementedError()

    @abstractmethod
    def delete_signal(self, data):
        """ Delete this signal and all associated data.

        :returns: True if successful, False otherwise.
        """
        raise NotImplementedError()

    @abstractmethod
    def insert(self, data):
        """ Insert data.

        :param data: Dictionary mapping signal names to timeseries.
        :returns: True if successful, False otherwise.

        Timeseries consist of an epoch timestamp in microseconds followed
        by some data.

        >>> datastore.insert({
        ... 'SIGNAL_A': (
        ...                 (1409481110001000, 1.2),
        ...                 (1409481110002000, 1.5)
        ...             ),
        ... 'SIGNAL_B': (
        ...                 (1409481110001500, -2.1)
        ...             )
        ... })
        True
        """
        raise NotImplementedError()

    @abstractmethod
    def get_last_points(self, signals, num):
        """ Return the last N points for the given signals.

        :param signals: A list of signals.
        :param num: The number of points to fetch.
        :return: A dictionary mapping signals to points.

        >>> signal = datastore.get_last_points(['SIGNAL_A'], 10)
        {'SIGNAL_A': [[1409481110001000, 1.2], [1409481110002000, 1.5], ...]}
        """
        raise NotImplementedError()

    @abstractmethod
    def get_timeseries(self, signals, t0, t1, dt, aggregate, limit):
        """ Return a uniformly sampled time series in a given time interval.
        Can  downsample, aggregate, and limit the result.

        :param signals: A list of signals.
        :param t0: Start time in microseconds.
        :param t1: End time in microseconds.
        :param dt: Sample time in microseconds
        :param aggregate: Aggregate function to apply.
        :param limit: Maximum number of points per signal to return.
        :return: A dictionary mapping signals to points.
        """
        raise NotImplementedError()
