from .api import InsteonResource

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
