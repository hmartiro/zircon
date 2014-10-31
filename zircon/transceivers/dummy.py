"""

"""

import time
from math import sin

from zircon.transceivers.base import BaseTransceiver


class DummyTransceiver(BaseTransceiver):

    def __init__(self, signal_name='dummy', data_gen=lambda t: sin(t), dt=0.1):

        self.dt = dt
        self.signal_name = signal_name
        self.data_gen = data_gen

        self.t = 0
        self.last = time.time()

    def open(self):
        return True

    def close(self):
        return True

    def pause(self):

        now = time.time()
        dt_real = now - self.last - self.dt
        self.t += now - self.last
        self.last = now

        to_wait = max(min(self.dt - dt_real, self.dt), 0)
        time.sleep(to_wait)

    def read(self):

        self.pause()

        timestamp = int(time.time() * 1e6)
        val = self.data_gen(self.t)
        return timestamp, self.signal_name, val

    def write(self, data):
        print('[WRITE] {}'.format(data))
        return True


if __name__ == '__main__':

    from zircon.publishers.zeromq import ZMQPublisher
    from zircon.reporters.base import Reporter
    from zircon.transformers.common import *
    from math import sin, pi

    def signal_generator(t):
        return sin(2*pi*t/3.0)

    reporter = Reporter(
        transceiver=DummyTransceiver(
            signal_name='MY_SIGNAL',
            data_gen=signal_generator,
            dt=1.0/1000
        ),
        transformers=[
            TimedCombiner(dt=0.1),
            Pickler(),
            Compressor()
        ],
        publisher=ZMQPublisher()
    )
    reporter.run()
