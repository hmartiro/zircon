"""

"""

from abc import ABCMeta, abstractmethod

from zircon.transformers.base import Transformer
from zircon.subscribers.zeromq import ZMQSubscriber
from zircon.datastores.influx import InfluxDatastore


class BaseInjector():

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


class Injector(BaseInjector):

    def __init__(self, subscriber=None, transformers=None, datastore=None):

        if subscriber:
            self.subscriber = subscriber
        else:
            self.subscriber = ZMQSubscriber()

        if transformers:
            self.transformers = transformers
        else:
            self.transformers = [Transformer()]

        if datastore:
            self.datastore = datastore
        else:
            self.datastore = InfluxDatastore()

        for i in range(len(self.transformers) - 1):
            self.transformers[i].set_callback(self.transformers[i+1].push)

        self.transformers[-1].set_callback(self.datastore.insert)

    def open(self):
        self.subscriber.open()

    def step(self):

        msg = self.subscriber.receive()

        if msg:
            self.transformers[0].push(msg)

    def run(self):

        self.open()

        while True:
            self.step()
