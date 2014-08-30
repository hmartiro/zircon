"""

"""

from zircon.publishers.base import BasePublisher


class DummyPublisher(BasePublisher):

    def __init__(self):
        pass

    def open(self):
        return True

    def close(self):
        return True

    def send(self, msg):
        print('[SENT] {}'.format(msg))
        return True
