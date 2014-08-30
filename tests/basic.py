from zircon.tranceivers.dummy import DummyTranceiver
from zircon.transformers.base import Transformer
from zircon.publishers.dummy import DummyPublisher

from zircon.reporters.base import Reporter

r = Reporter(
    tranceiver=DummyTranceiver(data='hi'),
    transformers=[Transformer(), Transformer(), Transformer()],
    publisher=DummyPublisher()
)

r.run()
