# Home Control - Server

Written in a server-client format with the intention to have the server side being run 24/7 on a Raspberry Pi, while separate clients can be written for different devices and systems.

Where possible, all commands are sent over the internal network. Some devices (eg Nest) are controlled using APIs that are only accessible over the internet. Commands are received over the network using the bottle python package.

<h4>Bundles that have been developed:</h4>

<p>Devices</p>
- LG TV control
- Virgin Media TiVo control

<p>Accounts</p>
- Nest (thermostat & smoke detectors)

<p>Info Services</p>
- Weather forecast (metoffice.gov.uk)
- TV Listings (bleb.org)

<br>
<h4>Bundles currently under developed:</h4>
- iCloud

<hr>

<h3>API Guide</h3>

<h5>Data requests</h5>
<p><code>GET</code> <code>/data/device/{room_id}/{device_id}/{resource_requested}</code></p>
<p>Request data for/from a particular device as requested by the {room_id} and {device_id} variables. {resource_requested} indicates the resource requested from the device. Further documentation to be produced for this.</p>
<p><code>GET</code> <code>/data/account/{account_id}/{resource_requested}</code></p>
<p>Request data for/from a particular account as requested by the {account_id} variable. {resource_requested} indicates the resource requested from the device. Further documentation to be produced for this.</p>
<p><code>GET</code> <code>/data/info/{service}/{resource_requested}</code></p>
<p>Request data for/from a particular information service as requested by the {service} variable. {resource_requested} indicates the resource requested from the device. Further documentation to be produced for this.</p>
<h5>Handle commands</h5>
<p><code>POST</code> <code>/command/device/{room_id}/{device_id}</code></p>
<p>Submit commands to the server for relaying to the particular device as requested by the {room_id} and {device_id} variables. Query parameters identify the command to be sent (<code>command</code>) and others that are device or command specific. Further documentation to be produced for this.</p>
<p><code>POST</code> <code>/command/account/{account_id}</code></p>
<p>Submit commands to the server for relaying to the particular account as requested by the {account_id} variable. Query parameters identify the command to be sent (<code>command</code>) and others that are device or command specific. Further documentation to be produced for this.</p>
<h5>Image requests</h5>
<p><code>GET</code> <code>/img/{category}/{filename:re:.*\.png}</code></p>
<p>Returns image as defined by pre-set HTML pages.</p>

<hr>

<h3>Required python packages</h3>
<p>The following python packages require installation on the target system:
<br>
bottle: <code>http://bottlepy.org/docs/dev/index.html</code>
<br>
requests: <code>http://docs.python-requests.org/en/master/</code>
<br>
pyicloud: <code>https://pypi.python.org/pypi/pyicloud</code>
</p>
