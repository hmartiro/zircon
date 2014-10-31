"""

"""

from zircon.transceivers.dummy import DummyTransceiver
from zircon.publishers.zeromq import ZMQPublisher
from zircon.reporters.base import Reporter
from zircon.transformers.common import *
from math import sin, pi


# Generated signal
def sine_wave(t):
    return sin(2*pi*t/3.0)

# Sampling frequency
freq = 1000

reporter = Reporter(
    transceiver=DummyTransceiver(
        signal_name='MY_SIGNAL',
        data_gen=sine_wave,
        dt=1.0/freq
    ),
    transformers=[
        TimedCombiner(dt=0.1),
        Pickler(),
        Compressor()
    ],
    publisher=ZMQPublisher()
)
reporter.run()
