"""

"""

from abc import ABCMeta, abstractmethod


class BaseSubscriber():

    __metaclass__ = ABCMeta

    @abstractmethod
    def open(self):
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        raise NotImplementedError()

    @abstractmethod
    def receive(self):
        raise NotImplementedError()
