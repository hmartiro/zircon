"""

"""

from abc import ABCMeta, abstractmethod


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

    def __init__(self, subscriber, decoder, datastore):

        self.subscriber = subscriber
        self.decoder = decoder
        self.datastore = datastore

        self.decoder.set_callback(self.datastore.insert)

    def open(self):
        self.subscriber.open()

    def step(self):

        msg = self.subscriber.receive()

        if msg:
            self.decoder.push(msg)

    def run(self):

        self.open()

        while True:
            self.step()
