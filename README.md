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

<hr>
<h3>API Guide</h3>
<p>
<code>GET</code> <code>/web/{page}</code>
<br>Returns a HTML page dependant on the variable {page}. Pages include home, tvguide and about.</p>
<br><p>
<code>GET</code> <code>/web/device/{grp_num}/{dvc_num}</code>
<br>Returns a HTML page created for the particular device as requested by the {grp_num} and {dvc_num} variables.
</p><br><p>
<code>GET</code> <code>/web/settings/{page}</code>
<br>Returns a HTML page for creating/amending the configuration for the server. Page returned dependant on the {page} variable, including devices and tvguide. Only accessible if user has admin rights.
</p><br><p>
<code>GET</code> <code>/web/settings?gethtml={html_request}&...</code>
<br>Used by the settings page /web/settings/devices for individual components when added by user.
<br>Additional query parameters dependant on value of <code>gethtml</code>:
<br>'group': <code>grpnum</code> (0,1,etc)
<br>'selection': <code>grpnum</code> (0,1,etc) & <code>dvcnum</code> (0,1,etc)
<br>'device': <code>grpnum</code> (0,1,etc), <code>dvcnum</code> (0,1,etc) & <code>device</code> (eg. tivo, nest)
</p><br><p>
<code>GET</code> <code>/web/preferences/{page}</code>
<br>Only one value available at present for {page} - tvguide. Returns a page for the logged in user to choose their favourite channels for showing in channel lists.
</p><br><p>
<code>GET</code> <code>/web/static/{folder}/{filename}</code>
<br>Returns static files such as css, js and fonts/glyphicons.
</p><br><p>
<code>POST/GET</code> <code>/command/{grp_num}/{dvc_num}</code>
<br>Submit commands to the server for relaying to the particular device as requested by the {group_num} and {device_num} variables.. Query parameters identify the command to be sent (<code>command</code>) and others that are device or command specific. Further documentation to be produced for this.
</p><br><p>
<code>POST</code> <code>/settings/{category}</code>
<br>Used to submit and save the config/settings via a json payload. Variables for {category} include 'tvguide' and 'devices' and admin access is required.
</p><br><p>
<code>POST</code> <code>/preferences/{category}</code>
<br>Used to submit and save the user preferences via a json payload.
</p><br><p>
<code>GET</code> <code>/favicon.ico</code>
<br>Returns favicon for HTML pages.
</p><br><p>
<code>GET</code> <code>/img/{category}/{filename:re:.*\.png}</code>
<br>Returns image as defined by pre-set HTML pages.
</p><br><p>
<code>GET</code> <code>/web/login</code>
<br>Present login screen for user selection and logging in.
<code>GET</code> <code>/web/logout</code>
<br>Logs user out by deleting session cookie.
</p><br>

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
