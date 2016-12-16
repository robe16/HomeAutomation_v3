# Home Control - Server

Written in a server-client format with the intention to have the server side being run 24/7 on a Raspberry Pi, while separate clients can be written for different devices and systems.

Where possible, all commands are sent over the internal network. Some devices (eg Nest) are controlled using APIs that are only accessible over the internet. Commands are received over the network using the bottle package.

A web interface has also been developed that will dynamically be created on the fly when requested, and will allow for commands to be sent to the server for controlling devices and changing the server's device and settings configuration (stored as json).

Elements that have been developed:
- LG TV control
- Virgin Media TiVo control
- Nest (thermostat & smoke detectors)
- Weather forecast

Elements to be developed:
- TV Listings (radiotimes API decomissioned - replacement requirement)

Elements planned for development in future:
- Rocki music streamer
- Chromecast (audio)
- Utility accounts (start with OVO Energy)
- Lights and sockets (possibly with LightwaveRF)
- ...and anything else I can think of!!

<p>
<code>POST/GET</code> <code>/command/device/{room_id}/{device_id}</code>
<br>Submit commands to the server for relaying to the particular device as requested by the {room_id} and {device_id} variables. Query parameters identify the command to be sent (<code>command</code>) and others that are device or command specific. Further documentation to be produced for this.
</p><br><p>
<code>POST/GET</code> <code>/command/account/{account_id}</code>
<br>Submit commands to the server for relaying to the particular account as requested by the {account_id} variable. Query parameters identify the command to be sent (<code>command</code>) and others that are device or command specific. Further documentation to be produced for this.
</p><br><p>
<code>GET</code> <code>/img/{category}/{filename:re:.*\.png}</code>
<br>Returns image as defined by pre-set HTML pages.
</p><br

<hr>

<h3>Required python packages</h3>
<p>The following python packages require installation on the target system:
<br>
bottle:
<code>http://bottlepy.org/docs/dev/index.html</code>
<br>
requests:
<code>http://docs.python-requests.org/en/master/</code>
</p>
