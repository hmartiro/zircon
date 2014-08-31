"""

"""

from abc import ABCMeta, abstractmethod


class BaseTransformer():
    """ Abstract base class defining the Transformer interface.

    A Transformer takes in messages, applies some transformation, and spits
    them back out. It is a general piece of middleware in a data stream that
    can be used to compress/decompress, encode/decode, or split/combine
    messages in a data pipeline.

    **Usage**::

        def process(msg):
            do_something(msg)

        t = MyTransformer()
        t.set_callback(process)

        for msg in messages:
            t.push(msg)

    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def set_callback(self, callback):
        """ Set a function to be invoked for each outputted message.
        """
        raise NotImplementedError()

    @abstractmethod
    def push(self, msg):
        """ Feed in a message.
        """
        raise NotImplementedError()


class Transformer(BaseTransformer):
    """ Transformer that acts as a pass-through, invoking the callback for
    each message received with no alterations.

    Extend this and override :func:`push` to implement a Transformer.
    """

    def __init__(self):
        self.callback = None

    def set_callback(self, callback):
        self.callback = callback

    def output(self, msg):
        """ If I have a callback, invoke it.
        """
        if self.callback:
            self.callback(msg)

    def push(self, msg):
        """ Output exactly what I receive.
        """
        self.output(msg)


