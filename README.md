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
