"""

"""

from abc import ABCMeta, abstractmethod


class BaseReporter():

    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self):
        raise NotImplementedError()


class Reporter(BaseReporter):

    def __init__(self, tranceiver, parser, publisher):

        self.tranceiver = tranceiver
        self.parser = parser
        self.publisher = publisher

    def run(self):

        self.tranceiver.open()
        self.publisher.open()

        self.parser.set_callback(self.publisher.send)

        while True:

            raw_data = self.tranceiver.read()

            if raw_data:
                self.parser.push(raw_data)
