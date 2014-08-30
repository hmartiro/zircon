"""

"""

import time

from zircon.subscribers.base import BaseSubscriber


class DummySubscriber(BaseSubscriber):

    def __init__(self, msg=None, dt=0.5):
        self.msg = msg
        self.dt = dt

    def open(self):
        return True

    def close(self):
        return True

    def receive(self):

        time.sleep(self.dt)
        return self.msg
