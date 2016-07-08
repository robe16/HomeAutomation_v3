# HomeAutomation v3

Written in a server-client format with the intention to have the server side being run 24/7 on a Raspberry Pi, while seperate clients can be written for different devices and systems.

Where possible, all commands are sent over the internal network. Some devices (eg Nest) are controlled using APIs that are only accessible over the internet. Commands are received over the network using the bottle package.

A web interface has also been developed that will dynamically be created on the fly when requested, and will allow for commands to be sent to the server for controlling devices and changing the server's device and settings configuration (stored as json).

Elements that have been developed:
- LG TV control
- Virgin Media TiVo control
- Nest (thermostat & smoke detectors)

Elements to be developed:
- TV Listings (radiotimes API decomissioned - replacement requirement)

Elements planned for development in future:
- Rocki music streamer
- Chromecast (audio)
- Utility accounts (start with OVO Energy)
- Lights and sockets (possibly with LightwaveRF)
- Weather forecasts for locality (post code based?)
- ...and anything else I can think of!!

The following python packages require installation on the target system:
<br>
bottle:
<code>http://bottlepy.org/docs/dev/index.html</code>
<br>
requests:
<code>http://docs.python-requests.org/en/master/</code>
