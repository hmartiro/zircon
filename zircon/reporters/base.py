"""

"""

from zircon.transformers.base import Transformer
from zircon.publishers.zeromq import ZMQPublisher


class Reporter():
    """ A Reporter continuously reads data from a Tranceiver, feeds it through
    a row of Transformers, and broadcasts the result using a Publisher.

    When creating a Reporter, you supply instances of a Tranceiver,
    one or more Transformers, and a Publisher. If not specified,
    a pass-through Transformer and the default Publisher are used.

    **Usage**::

        reporter = Reporter(
            tranceiver=MyTranceiver(),
            transformers=[MyDecoder(), MyCompressor(), ...],
            publisher=MyPublisher()
        )

    A Reporter can be run as its own process::

        reporter.run()

    Or stepped through by an external engine::

        reporter.open()
        while not done:
            reporter.step()
    """

    def __init__(self, tranceiver, transformers=None, publisher=None):

        self.tranceiver = tranceiver

        if transformers:
            self.transformers = transformers
        else:
            self.transformers = [Transformer()]

        if publisher:
            self.publisher = publisher
        else:
            self.publisher = ZMQPublisher()

        for i in range(len(self.transformers) - 1):
            self.transformers[i].set_callback(self.transformers[i+1].push)

        self.transformers[-1].set_callback(self.publisher.send)

    def open(self):
        """ Initialize the Tranceiver and Publisher.
        """

        self.tranceiver.open()
        self.publisher.open()

    def step(self):
        """ Read data and feed it into the first Transformer.
        """

        raw_data = self.tranceiver.read()

        if raw_data:
            self.transformers[0].push(raw_data)

    def run(self):
        """ Initialize components and start broadcasting.
        """

        self.open()

        while True:
            self.step()
