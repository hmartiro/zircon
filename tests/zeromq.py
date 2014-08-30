"""

"""

from zircon.tranceivers.dummy import DummyTranceiver
from zircon.transformers.base import Transformer
from zircon.publishers.zeromq import ZMQPublisher
from zircon.subscribers.zeromq import ZMQSubscriber
from zircon.datastores.dummy import DummyDatastore

from zircon.reporters.base import Reporter
from zircon.injectors.base import Injector

reporter = Reporter(
    tranceiver=DummyTranceiver(data='hi', dt=0.1),
    transformers=[Transformer()],
    publisher=ZMQPublisher()
)

injector = Injector(
    subscriber=ZMQSubscriber(),
    transformers=[Transformer()],
    datastore=DummyDatastore()
)

reporter.open()
injector.open()

while True:
    reporter.step()
    injector.step()
