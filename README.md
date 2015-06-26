# insteon-python-lib
My initial concept for a Python library for interfacing with the Insteon Hub2 Restful API http://docs.insteon.apiary.io/

# Status
Currently abandoned - The Hub2 is not a robust platform for Insteon device management, it primarily focuses on device control.  Best I can tell, Insteon expects you to manual link devices with limited support for software linking a device to the hub itself.

My hope had been that the hub would provide robust device management (linking, setting default states, and setting unique device parameters).  Since device management is highly platform specific, handling this in a Insteon defined world would be best.  

This library was meant to provide a standardized bridge to the Insteon platform.  This would enable home automation systems such as Home Assistant https://github.com/balloob/home-assistant to add insteon support.

Sadly, if the hub does not provide robust device management, there is little value for device control through the hub.
