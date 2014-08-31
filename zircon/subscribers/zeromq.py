"""

"""

import zmq
import cPickle as pickle

from zircon.subscribers.base import BaseSubscriber


class ZMQSubscriber(BaseSubscriber):

    def __init__(self, host='localhost', port=8811, zmq_type=zmq.SUB):

        self.host = host
        self.port = port
        self.zmq_type = zmq_type

        self.URI = 'tcp://{}:{}'.format(host, port)

        self.context = zmq.Context()
        self.sock = self.context.socket(self.zmq_type)

        if self.zmq_type == zmq.SUB:
            self.sock.setsockopt(zmq.SUBSCRIBE, '')

    def open(self):
        self.sock.connect(self.URI)
        return True

    def close(self):
        self.sock.disconnect(self.URI)
        return True

    def receive(self):
        return self.sock.recv()
