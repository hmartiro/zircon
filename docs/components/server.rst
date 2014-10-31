..  _server:

Socket.IO Server
================

.. NOTE::
   This documentation is a work in progress. Browse the code in ``zircon/zircon/frontend``.

Zircon's backend server provides a Socket.IO interface to query information
from a Datastore. It allows real-time bidirectional event-based communication
between a client application that receives data and the Datastore. Works for
web or native applications, on any platform. Allows powerful querying of
every recorded data point, by default for the past week.
