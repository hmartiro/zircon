"""

"""

from abc import ABCMeta, abstractmethod


class BaseTransceiver():
    """ Abstract base class defining the Transceiver interface.

    A Transceiver reads and/or writes to some source. It is the lowest-level
    component in zircon, which would for example interface with a CAN bus,
    serial port, or XBee.

    **Usage**::

        t = MyTransceiver()
        t.open()

        while not done:
            data = t.read()
            process(data)

        t.close()

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
    def read(self):
        """ Return data read from the connection, or None.
        """
        raise NotImplementedError()

    @abstractmethod
    def write(self, data):
        """ Write data to the connection.
        """
        raise NotImplementedError()
