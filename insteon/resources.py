from .api import InsteonResource, InsteonCommandable

class House(InsteonResource):
    resource_name="houses"
    _settables = (
        'InsteonHubID', 'HouseName', 'City', 'DHCP', 'DaylightSavings'
    )
    _properties = (
        'InsteonHubID','HouseName','City','DHCP','DaylightSavings',
        'HubType','HubUsername','HubPassword','IP','Port','Gateway',
        'Mask','Mac','BinVer','PLMVer','FirmwareVer','HouseID','IconID'
    )

class Account(InsteonResource):
    resource_name="accounts"
    #TODO add DefaultAddress
    _settables = (
        'Username', 'Email', 'FirstName', 'LastName', 'Suffix',
        'Phone'
    )
    _properties = (
        'AccountID', 'Username', 'Email', 'FirstName', 'LastName',
        'Suffix', 'Phone'
    )

class Contact(InsteonResource):
    resource_name="contacts"
    _settables = (
        'ContactName', 'NotifyTo', 'ContactType', 'Prefered'
    )
    _properties = (
        'ContactName', 'NotifyTo', 'ContactType', 'Prefered'
    )

class Device(InsteonCommandable):
    resource_name="devices"
    _settables = (
        'HouseID', 'DeviceName', 'InsteonID', 'FirmwareVersion', 'OnTime', 'OffTime',
        'TimerEnabled', 'Group', 'DeviceType', 'DevCat', 'SubCat', 'AutoStatus', 'CustomOn',
        'CustomOff', 'EnableCustomOn', 'EnableCustomOff', 'DimLevel', 'RampRate', 'OperationalFlags',
        'LEDLevel', 'AlertsEnabled', 'AlertOn', 'AlertOff', 'Favorite', 'Humidity', 'DayMask',
        'LinkWithHub', 'BeepOnPress', 'LocalProgramLock', 'BlinkOnTraffic', 'ErrorBlink',
        'ConfiguredGroups', 'InsteonEngine', 'SerialNumber', 'Manufacturer', 'ProductType',
        'User', 'UserID', 'AccessToken', 'IpAddress', 'Port', 'GroupList', 'DeviceID'
    )
    _properties = (
        'HouseID', 'DeviceName', 'InsteonID', 'FirmwareVersion', 'OnTime', 'OffTime',
        'TimerEnabled', 'Group', 'DeviceType', 'DevCat', 'SubCat', 'AutoStatus', 'CustomOn',
        'CustomOff', 'EnableCustomOn', 'EnableCustomOff', 'DimLevel', 'RampRate', 'OperationalFlags',
        'LEDLevel', 'AlertsEnabled', 'AlertOn', 'AlertOff', 'Favorite', 'Humidity', 'DayMask',
        'LinkWithHub', 'BeepOnPress', 'LocalProgramLock', 'BlinkOnTraffic', 'ErrorBlink',
        'ConfiguredGroups', 'InsteonEngine', 'SerialNumber', 'Manufacturer', 'ProductType',
        'User', 'UserID', 'AccessToken', 'IpAddress', 'Port', 'GroupList', 'DeviceID'
    )
