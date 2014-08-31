"""

"""

from zircon.transformers.common import Unpickler
from zircon.subscribers.zeromq import ZMQSubscriber
from zircon.datastores.influx import InfluxDatastore


class Injector():
    """ An Injector listens for data from a Reporter, feeds it through a row of
    Transformers, and inserts the result into a Datastore.

    When creating an Injector, you supply instances of a Subscriber,
    one or more Transformers, and a Datastore. If not specified,
    a pickling Transformer and the default Subscriber and Datastore are
    used.

    **Usage**::

        injector = Injector(
            subscriber=MySubscriber(),
            transformers=[MyDecompressor(), MyFormatter(), ...],
            datastore=MyDatastore()
        )

    An Injector can be run as its own process::

        injector.run()

    Or stepped through by an external engine::

        injector.open()
        while not done:
            injector.step()
    """

    def __init__(self, subscriber=None, transformers=None, datastore=None):

        if subscriber:
            self.subscriber = subscriber
        else:
            self.subscriber = ZMQSubscriber()

        if transformers:
            self.transformers = transformers
        else:
            self.transformers = [Unpickler()]

        if datastore:
            self.datastore = datastore
        else:
            self.datastore = InfluxDatastore()

        for i in range(len(self.transformers) - 1):
            self.transformers[i].set_callback(self.transformers[i+1].push)

        self.transformers[-1].set_callback(self.datastore.insert)

    def open(self):
        """ Initialize the Subscriber.
        """
        self.subscriber.open()

    def step(self):
        """ Receive data and feed it into the first Transformer.
        """

        msg = self.subscriber.receive()

        if msg:
            self.transformers[0].push(msg)

    def run(self):
        """ Initialize components and start listening.
        """

        self.open()

        while True:
            self.step()
