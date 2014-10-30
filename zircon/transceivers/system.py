"""

"""

import time
import psutil

from zircon.transceivers.base import BaseTransceiver


class SystemTransceiver(BaseTransceiver):

    def __init__(self, dt=0.1):

        self.dt = dt

    def open(self):
        return True

    def close(self):
        return True

    def read(self):

        data = []
        timestamp = int(time.time() * 1e6)

        cpu = psutil.cpu_percent(interval=self.dt, percpu=True)

        [data.append((timestamp, 'CPU_{}_USAGE'.format(i), val)) for i, val in enumerate(cpu)]

        connections = len(psutil.net_connections())
        data.append((timestamp, 'NUM_CONNECTIONS', connections))

        net_io = psutil.net_io_counters(True)
        disk_io = psutil.disk_io_counters(True)
        [data.append((timestamp, '{}_SENT'.format(c.upper()), net_io[c].bytes_sent)) for c in net_io]
        [data.append((timestamp, '{}_RECV'.format(c.upper()), net_io[c].bytes_recv)) for c in net_io]
        [data.append((timestamp, '{}_READ'.format(d.upper()), disk_io[d].read_bytes)) for d in disk_io]
        [data.append((timestamp, '{}_WRITE'.format(d.upper()), disk_io[d].write_bytes)) for d in disk_io]
        return data

    def write(self, data):
        print('[WRITE] {}'.format(data))
        return True

if __name__ == '__main__':

    from zircon.publishers.zeromq import ZMQPublisher
    from zircon.reporters.base import Reporter

    from zircon.transformers.common import *

    reporter = Reporter(
        transceiver=SystemTransceiver(
        ),
        transformers=[
            Splitter(),
            TimedCombiner(dt=0.1),
            Pickler(),
            Compressor()
        ],
        publisher=ZMQPublisher()
    )
    reporter.run()
