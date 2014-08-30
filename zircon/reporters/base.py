"""

"""

from abc import ABCMeta, abstractmethod


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

    def __init__(self, tranceiver, parser, publisher):

        self.tranceiver = tranceiver
        self.parser = parser
        self.publisher = publisher

        self.parser.set_callback(self.publisher.send)

    def open(self):

        self.tranceiver.open()
        self.publisher.open()

    def step(self):

        raw_data = self.tranceiver.read()

        if raw_data:
            self.parser.push(raw_data)

    def run(self):

        self.open()

        while True:
            self.step()
