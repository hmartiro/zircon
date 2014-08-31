"""

"""

from abc import ABCMeta, abstractmethod


class BasePublisher():
    """ Abstract base class defining the Publisher interface.

    A Publisher broadcasts data in some form, to be picked up by one or more
    Subscribers. It is used by Reporters to communicate with Injectors.

    **Usage**::

        p = MyPublisher()
        p.open()

        while not done:
            msg = get_data()
            p.send(msg)

        p.close()

    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def open(self):
        """ Open the connection.
        """
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        """ Close the connection.
        """
        raise NotImplementedError()

    @abstractmethod
    def send(self, msg):
        """ Broadcast a message.
        """
        raise NotImplementedError()
