"""

"""

from abc import ABCMeta, abstractmethod


class BaseParser():

    __metaclass__ = ABCMeta

    @abstractmethod
    def set_callback(self, callback):
        raise NotImplementedError()

    @abstractmethod
    def push(self, data):
        raise NotImplementedError()
