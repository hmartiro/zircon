"""

"""

__title__ = 'zircon'
__version__ = '0.1.0'
__author = 'Hayk Martirosyan'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014 Hayk Martirosyan'

import logging

# TODO setup global logger

from zircon.reporters import base

r = base.Reporter()

from zircon.reporters.base import Reporter

r = Reporter()

from zircon.reporters import Reporter

from zircon.tranceivers.komodo import KomodoTranceiver
from zircon.parsers.base import PassThroughParser
from zircon.publishers import Publisher

r = Reporter(
    tranceiver=KomodoTranceiver(),
    parser=PassThroughParser(),
    publisher=
)
