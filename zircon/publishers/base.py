"""

"""

from abc import ABCMeta, abstractmethod


class BasePublisher():

    __metaclass__ = ABCMeta

    @abstractmethod
    def open(self):
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        raise NotImplementedError()

    @abstractmethod
    def send(self, msg):
        raise NotImplementedError()
