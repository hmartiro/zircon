"""

"""

from abc import ABCMeta, abstractmethod


class BaseSubscriber():
    """ Abstract base class defining the Subscriber interface.

    A Subscriber receives data from a Publisher. It is used by Injectors
    to listen to Reporters.

    **Usage**::

        s = MySubscriber()
        s.open()

        while not done:
            msg = s.receive()
            process(msg)

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
    def receive(self):
        """ Receive a message.
        """
        raise NotImplementedError()
