"""

"""

from abc import ABCMeta, abstractmethod


class BaseInjector():

    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self):
        raise NotImplementedError()


class Injector(BaseInjector):

    def __init__(self, subscriber, decoder, datastore):

        self.subscriber = subscriber
        self.decoder = decoder
        self.datastore = datastore

    def run(self):

        self.subscriber.open()

        self.decoder.set_callback(self.datastore.insert)

        while True:

            msg = self.subscriber.read()

            if msg:
                self.decoder.push(msg)
