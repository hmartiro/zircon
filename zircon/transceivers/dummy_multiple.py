"""

"""

import time
import math

from zircon.transceivers.base import BaseTransceiver


class DummyMultipleTransceiver(BaseTransceiver):

    def __init__(self, signals=None, dt=0.1):

        self.dt = dt
        self.t = 0
        self.t_real = time.time()

        self.signals = signals
        if not self.signals:
            self.signals = {'sin': math.sin}

    def open(self):
        return True

    def close(self):
        return True

    def read(self):

        time.sleep(self.dt)
        now = time.time()
        self.t += now - self.t_real
        self.t_real = now

        timestamp = int(now * 1e6)
        data = [(timestamp, name, func(self.t)) for name, func in self.signals.items()]

        return data

    def write(self, data):
        print('[WRITE] {}'.format(data))
        return True


if __name__ == '__main__':

    from zircon.publishers.zeromq import ZMQPublisher
    from zircon.reporters.base import Reporter

    from zircon.transformers.common import *

    from math import sin, pi
    from random import gauss

    reporter = Reporter(
        transceiver=DummyMultipleTransceiver(
            signals={
                'IMU_X': lambda x: 1.0 * sin(2*pi*(x/3.0 + 1)) + gauss(0, 0.2),
                'IMU_Y': lambda x: 1.5 * sin(2*pi*x/2.5) + gauss(0, 0.2),
                'IMU_Z': lambda x: 1.3 * sin(2*pi*x/2.8) + gauss(0, 0.3),
                'IMU_X_FILTERED': lambda x: 1.0 * sin(2*pi*(x/3.0 + 1)),
                'IMU_Y_FILTERED': lambda x: 1.5 * sin(2*pi*x/2.5),
                'IMU_Z_FILTERED': lambda x: 1.3 * sin(2*pi*x/2.8),
            },
            dt=0.01,
        ),
        transformers=[
            Splitter(),
            TimedCombiner(dt=0.1),
            Pickler(),
            Compressor()
        ],
        publisher=ZMQPublisher()
    )
    reporter.run()
