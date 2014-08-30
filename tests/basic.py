from zircon.tranceivers.dummy import DummyTranceiver
from zircon.parsers.dummy import DummyParser
from zircon.publishers.dummy import DummyPublisher

from zircon.reporters.base import Reporter

r = Reporter(
    tranceiver=DummyTranceiver(data='hi'),
    parser=DummyParser(),
    publisher=DummyPublisher()
)

r.run()
