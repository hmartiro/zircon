"""

"""

from abc import ABCMeta, abstractmethod


class BaseTransformer():

    __metaclass__ = ABCMeta

    @abstractmethod
    def set_callback(self, callback):
        raise NotImplementedError()

    @abstractmethod
    def push(self, data):
        raise NotImplementedError()


class Transformer(BaseTransformer):

    def __init__(self):
        self.callback = None

    def set_callback(self, callback):
        self.callback = callback

    def push(self, data):
        if self.callback:
            self.callback(data)
