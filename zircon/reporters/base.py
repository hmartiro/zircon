"""

"""

from zircon.transformers.common import Pickler
from zircon.publishers.zeromq import ZMQPublisher


class Reporter():
    """ A Reporter continuously reads data from a Transceiver, feeds it through
    a row of Transformers, and broadcasts the result using a Publisher.

    When creating a Reporter, you supply instances of a Transceiver,
    one or more Transformers, and a Publisher. If not specified,
    a pickling Transformer and the default Publisher are used.

    **Usage**::

        reporter = Reporter(
            transceiver=MyTransceiver(),
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

    def __init__(self, transceiver, transformers=None, publisher=None):

        self.transceiver = transceiver

        if transformers:
            self.transformers = transformers
        else:
            self.transformers = [Pickler()]

        if publisher:
            self.publisher = publisher
        else:
            self.publisher = ZMQPublisher()

        for i in range(len(self.transformers) - 1):
            self.transformers[i].set_callback(self.transformers[i+1].push)

        self.transformers[-1].set_callback(self.publisher.send)

    def open(self):
        """ Initialize the Transceiver and Publisher.
        """

        success = self.transceiver.open()
        if not success:
            return False

        success = self.publisher.open()
        if not success:
            return False

        return True

    def step(self):
        """ Read data and feed it into the first Transformer.
        """

        raw_data = self.transceiver.read()

        if raw_data is not None:
            self.transformers[0].push(raw_data)

    def run(self):
        """ Initialize components and start broadcasting.
        """

        success = self.open()
        if not success:
            print('Failed to initialize!')
            return

        while True:
            self.step()
