"""

"""

import zlib
import cPickle as pickle

import time

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
    """ Capitalize string-like messages.
    """
    def push(self, msg):
        self.output(msg.upper())


class Lowercaser(Transformer):
    """ Lowercase string-like messages.
    """
    def push(self, msg):
        self.output(msg.lower())


class Pickler(Transformer):
    """ Pickle messages with the latest protocol.
    """
    def push(self, msg):
        serialized_msg = pickle.dumps(msg)
        from pympler.asizeof import asizeof
        print('unpickled: {}, pickled: {}'.format(
            asizeof(msg),
            asizeof(serialized_msg)
        ))
        self.output(serialized_msg)


class Unpickler(Transformer):
    """ Unpickle messages with the latest protocol.
    """
    def push(self, msg):
        self.output(pickle.loads(msg))


class Compressor(Transformer):
    """ Compress messages using zlib.
    """
    def push(self, msg):

        compressed_msg = zlib.compress(msg)
        from pympler.asizeof import asizeof
        print('uncompressed: {}, compressed: {}'.format(
            asizeof(msg),
            asizeof(compressed_msg)
        ))
        self.output(compressed_msg)


class Decompressor(Transformer):
    """ Decompress messages using zlib.
    """
    def push(self, compressed_msg):
        self.output(zlib.decompress(compressed_msg))


class TimedCombiner(Transformer):
    """ Convert individual data points into a dictionary
    of signal names to time series, outputted at a regular
    interval.

    Input: (12345, 'MYSIGNAL', -5.2), (12346, 'MYSIGNAL', 1.3), ...
    Output: {'MYSIGNAL': ((12345, -5.2), (12346, 1.3))}
    """
    def __init__(self, dt=0.1):

        Transformer.__init__(self)

        self.dt = dt
        self.data_to_save = {}
        self.last_saved = time.time()

    def push(self, msg):

        signal_name = msg[1]
        if signal_name not in self.data_to_save:
            self.data_to_save[signal_name] = []
        self.data_to_save[signal_name].append((msg[0], msg[2]))

        now = time.time()
        if now - self.last_saved > self.dt:
            self.output(self.data_to_save)
            self.last_saved = now
            self.data_to_save = {}


class Printer(Transformer):
    """ Prints messages and passes them on unaltered.
    """
    def __init__(self, prefix=None):
        Transformer.__init__(self)
        self.prefix = prefix

    def push(self, msg):
        if self.prefix:
            print('[{}] {}'.format(self.prefix, msg))
        else:
            print(msg)
        self.output(msg)


class Timer(Transformer):
    """ Prints the time between messages, and passes them on unaltered.
    """
    def __init__(self):
        Transformer.__init__(self)
        self.t = time.time()

    def push(self, msg):
        now = time.time()
        print('Time since last message: {:03f}s'.format(now - self.t))
        self.t = now
        self.output(msg)
