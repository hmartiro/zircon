"""

"""

from abc import ABCMeta, abstractmethod

from zircon.transformers.base import Transformer
from zircon.publishers.zeromq import ZMQPublisher


class BaseReporter():

    __metaclass__ = ABCMeta

    @abstractmethod
    def open(self):
        raise NotImplementedError()

    @abstractmethod
    def step(self):
        raise NotImplementedError()

    @abstractmethod
    def run(self):
        raise NotImplementedError()


class Reporter(BaseReporter):

    def __init__(self, tranceiver, transformers=None, publisher=None):

        self.tranceiver = tranceiver

        if transformers:
            self.transformers = transformers
        else:
            self.transformers = [Transformer()]

        if publisher:
            self.publisher = publisher
        else:
            self.publisher = ZMQPublisher()

        for i in range(len(self.transformers) - 1):
            self.transformers[i].set_callback(self.transformers[i+1].push)

        self.transformers[-1].set_callback(self.publisher.send)

    def open(self):

        self.tranceiver.open()
        self.publisher.open()

    def step(self):

        raw_data = self.tranceiver.read()

        if raw_data:
            self.transformers[0].push(raw_data)

    def run(self):

        self.open()

        while True:
            self.step()
