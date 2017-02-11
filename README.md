# Home Control - Server

<strong>Full documentation can be found at https://github.com/robe16/HomeControl-documentation/wiki/HomeControl-Server</strong>

Written in a server-client format with the intention to have the server side being run 24/7 on a Raspberry Pi, while separate clients can be written for different devices and systems.

Where possible, all commands are sent over the internal network. Some devices (eg Nest) are controlled using APIs that are only accessible over the internet. Commands are received over the network using the bottle python package.


<img src="https://github.com/robe16/HomeControl-documentation/blob/master/images/interfaces/img_e2e_high-level-design.jpg">
<h5>Figure: High level end to end design of HomeControl project</h5>

<h4>Bundles that have been developed:</h4>

<p>Devices</p>
- LG TV control
- Virgin Media TiVo control
- Nest (thermostat & smoke detectors)

<p>Info Services</p>
- Weather forecast (metoffice.gov.uk)
- TV Listings (bleb.org)

<img src="https://github.com/robe16/HomeControl-documentation/blob/master/images/interfaces/img_interfaces_server-devices.jpg">
<h5>Figure: Interfaces between server and devices/accounts/info sources</h5>

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
