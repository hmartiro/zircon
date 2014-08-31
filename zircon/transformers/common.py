"""

"""

import zlib
import cPickle as pickle

from zircon.transformers import base

# Copied from base for convenience
Transformer = base.Transformer


class Combiner(Transformer):
    """ Combine messages into a list, then send them out.
    """
    def __init__(self, limit):
        """
        :param limit: How many messages to combine.
        """
        Transformer.__init__(self)

        self.limit = limit
        self.messages = []

    def push(self, msg):

        self.messages.append(msg)

        if len(self.messages) >= self.limit:
            self.output(self.messages)
            self.messages = []


class Doubler(Transformer):
    """ Output each message twice.
    """
    def push(self, msg):
        self.output(msg)
        self.output(msg)


class Splitter(Transformer):
    """ Split messages into parts by iterating through them.
    """
    def push(self, msg):
        for part in msg:
            self.output(part)


class Uppercaser(Transformer):
    """ Capitalize messages.
    """
    def push(self, msg):
        self.output(msg.upper())


class Lowercaser(Transformer):
    """ Lowercase messages.
    """
    def push(self, msg):
        self.output(msg.lower())


class Pickler(Transformer):
    """ Pickle messages with the latest protocol.
    """
    def push(self, msg):

        serialized_msg = pickle.dumps(msg)
        import sys
        print('unpickled: {}, pickled: {}'.format(
            sys.getsizeof(msg),
            sys.getsizeof(serialized_msg)
        ))
        self.output(serialized_msg)


class Unpickler(Transformer):
    """ Unpickle messages with the latest protocol.
    """
    def push(self, msg):
        self.output(pickle.loads(msg))


class Compressor(Transformer):
    """ Compresses messages using zlib.
    """
    def push(self, msg):

        compressed_msg = zlib.compress(msg)
        import sys
        print('uncompressed: {}, compressed: {}'.format(
            sys.getsizeof(msg),
            sys.getsizeof(compressed_msg)
        ))
        self.output(compressed_msg)


class Decompressor(Transformer):
    """ Decompress messages using zlib.
    """
    def push(self, compressed_msg):
        self.output(zlib.decompress(compressed_msg))
