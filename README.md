zircon
======

Zircon is a lightweight open-source framework to intercept, store, analyze, and visualize high-speed signals in real-time using modern technologies. High-speed means thousands of messages per second and real-time means a latency of milliseconds to tens of milliseconds.

### Purpose

Zircon is designed to capture rapid streams of data in large communication networks like CAN busses and wireless meshes. This usually means sensor and actuator signals, but can be anything that boils down to events or time-series.

Zircon consists of extensible components that function individually or as a full stack solution. It can be used for decoding and logging, structured querying and analysis, plug-and-play real-time diagnostics, or for creating your own native or web-based applications.

Zircon is free and open-source, fast, platform-independent, easy to customize, and easy to integrate with your system. By default, Zircon uses InfluxDB for blazing-fast storage, ZeroMQ for local or remote reporting, and Socket.IO for streaming real-time data. It provides base classes and examples that can be extended to support any protocol or encoding. Really, give it a shot.

### Application Example

Steve is the lead engineer for a new hovercraft. His hovercraft contains ECUs for propulsion, sensing, power management, safety systems, and so on, which all communicate on a CAN bus. Steve's engineers spend a lot of their time monitoring and debugging the state of their respective systems and the messages they send/receive.

The engineers have various expensive, bulky, archaic, and/or proprietary software options for monitoring the bus. What they provide is the capability to interface with the bus, filter for certain types of messages, and log data. However, the engineers end up spending a lot of time watching the stream and manually decoding their protocols. Or worse, they have to pull raw data from log files, match up times, and hunt for something meaningful.

Steve installs Zircon on his laptop and writes a little code based on the provided examples. He launches the reporter and receiver processes, and pulls up the web interface. TBC.

### Components

+ *Sniffer* -
+ *Decoder* -
+ *Reader* -
+ *Parser* -
+ *Sender* -
+ *Receiver* -
+ *Decoder* -
+ *Database* -
