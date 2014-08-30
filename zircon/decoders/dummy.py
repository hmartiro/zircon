"""

"""

from zircon.decoders.base import BaseDecoder


class DummyDecoder(BaseDecoder):

    def __init__(self):
        self.callback = None

    def set_callback(self, callback):
        self.callback = callback

    def push(self, data):
        if self.callback:
            self.callback(data)
