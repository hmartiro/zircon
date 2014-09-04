"""

"""

from zircon.subscribers.zeromq import ZMQSubscriber
from zircon.datastores.influx import InfluxDatastore

from zircon.injectors.base import Injector

from zircon.transformers.common import *

injector = Injector(
    subscriber=ZMQSubscriber(),
    transformers=[
        Decompressor(),
        Unpickler(),
    ],
    datastore=InfluxDatastore()
)
injector.run()
