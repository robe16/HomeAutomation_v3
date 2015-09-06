# HomeAutomation v3

Rewrite of v2 of the Android application for home automation. v3 is being written in a server-client format with the intention to have the server side being run 24/7 on a Raspberry Pi, while seperate clients can be written for different devices and systems.

Where possible, all commands are sent over the internal network. Some devices (eg Nest) are controlled using APIs that are only accessible over the internet. Commands are recieved over the network using 'bottle.py'.

A web interface has also been developed that will dynamically be created on the fly when requested, and will allow for commands to be sent to the server for controlling devices and changing the server's device and settings configuration (stored as json).

Elements that have been developed:
- LG TV control
- Virgin Media TiVo control
- TV listings from RadioTimes

Elements to be developed:
- Nest thermostat
- Nest smoke detectors

Elements planned for development in future:
- Rocki music streamer
- Lights and sockets (possibly with LightwaveRF)
- Weather forecasts for locality (post code based?)
- ...and anything else I can think of!!
