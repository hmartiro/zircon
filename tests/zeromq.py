"""

"""

from zircon.tranceivers.dummy import DummyTranceiver
from zircon.parsers.dummy import DummyParser
from zircon.publishers.zeromq import ZMQPublisher

from zircon.subscribers.zeromq import ZMQSubscriber
from zircon.decoders.dummy import DummyDecoder
from zircon.datastores.dummy import DummyDatastore

from zircon.reporters.base import Reporter
from zircon.injectors.base import Injector

reporter = Reporter(
    tranceiver=DummyTranceiver(data='hi'),
    parser=DummyParser(),
    publisher=ZMQPublisher()
)

injector = Injector(
    subscriber=ZMQSubscriber(),
    decoder=DummyDecoder(),
    datastore=DummyDatastore()
)

reporter.open()
injector.open()

while True:
    reporter.step()
    injector.step()
