"""

"""

from zircon.transceivers.dummy import DummyTransceiver
from zircon.publishers.zeromq import ZMQPublisher
from zircon.reporters.base import Reporter

from zircon.transformers.common import *

reporter = Reporter(
    transceiver=DummyTransceiver(
        signal_name='dummy',
        dt=1/2000.
    ),
    transformers=[
        TimedCombiner(dt=0.1),
        Pickler(),
        Compressor()
    ],
    publisher=ZMQPublisher()
)
reporter.run()
