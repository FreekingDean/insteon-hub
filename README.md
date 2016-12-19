# insteon-hub
An initial concept for a Python library for interfacing with the Insteon Hub2 Restful API http://docs.insteon.apiary.io/

This is mostly based off https://github.com/krkeegan/insteon-hub-python-lib which seems to be abandoned.

In order to use this, you'll need to register for an Insteon [API key](http://www.insteon.com/become-an-insteon-developer).

## Installation
Install instructions can be found here https://pypi.python.org/pypi/insteon_hub

## Usage

### Initialize the object
```python
>>> import insteon
>>> i = insteon.Insteon("insteon_userid", "insteon_password", "insteon_api_key")
```

### Examine devices
```python
>>> i.devices
>>> i.devices[0]
>>> i.devices[0].DeviceName
```

*see [Devices](http://docs.insteon.apiary.io/#reference/devices) for other properties*

### Send a command
```python
>>> i.devices[0].send_command('on')
```
*see [Commands](http://docs.insteon.apiary.io/#reference/commands/commands-collection)*

### Streaming Data
```python
>>> i.houses[0].stream(auto_reconnect=True, devices_to_watch=i.devices)
```

This will auto update a cached status on each device from the insteon streaming endpoint.
It will auto reconnect every 60 seconds or so, Insteon has informed me they are
looking to increase the timeout on that endpoint. This will *NOT* report information
sent via API's you should either do a hard 'get_status' command every so often. It will
cache commands sent via THIS API.

*see [Streaming](http://docs.insteon.apiary.io/#reference/houses/house-device-activation-stream/retrieve-a-house-device-activation-stream)*

You can also add callbacks for a stream to get instant results.

```python
>>> i.houses[0].add_stream_callback(device, callback_method)
>>> i.houses[0].stream(auto_reconnect=True, devices_to_watch=i.devices)
```

This will send the parsed status to the `callback_method` as an argument.
