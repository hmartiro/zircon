"""

"""

import time
import random

from zircon.tranceivers.base import BaseTranceiver


class DummyTranceiver(BaseTranceiver):

    def __init__(self, signal_name='dummy', data_gen=None, dt=0.5):

        self.dt = dt
        self.signal_name = signal_name

        self.data_gen = data_gen
        if not self.data_gen:
            self.data_gen = lambda: random.uniform(-1, 1)

    def open(self):
        return True

    def close(self):
        return True

    def read(self):

        time.sleep(self.dt)

        if self.dt > 0:
            timestamp = int(time.time() * 1e6)
            val = self.data_gen()
            return timestamp, self.signal_name, val
        else:
            return None

    def write(self, data):
        print('[WRITE] {}'.format(data))
        return True
