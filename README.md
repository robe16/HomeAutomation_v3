# HomeAutomation v3

Rewrite of v2 of the Android application for home automation. v3 is being written in a server-client format with the intention to have the server side being run 24/7 on a Raspberry Pi, while seperate clients can be written for different devices and systems.

Where possible, all commands are sent over the internal network. Some devices (eg Nest) are controlled using APIs that are only accessible over the internet.

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

****************************************************************
NOTES ON CODING STYLE AND NAMING VARIABLES
****************************************************************
Perhaps through my OCD or through habits I have created for myself from being self taught, I have a standard way to define variable names.

The first few letters are always capitals and identify what the variable has been declared as. This is followed by lowercase characters to describe what the variable is used for.

For example:

Strings start with STR... (e.g. STRipaddress, STRdevicename)

Integers start with INT... (e.g. INTcount, INTkey)

Buttons start with BTN... (e.g. BTNok, BTNclose)

Images start with IMG... (e.g. IMGlogo, IMGchannel)

****************************************************************
