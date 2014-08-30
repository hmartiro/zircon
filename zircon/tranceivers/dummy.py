"""

"""

import time

from zircon.tranceivers.base import BaseTranceiver


class DummyTranceiver(BaseTranceiver):

    def __init__(self, data=None, dt=0.5):

        self.data = data
        self.dt = dt

    def open(self):
        return True

    def close(self):
        return True

    def read(self):
        time.sleep(self.dt)
        return self.data

    def write(self, data):
        return True
