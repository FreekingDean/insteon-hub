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

    def stream(self, auto_reconnect=False, devices_to_watch={}):
        self._api_iface.stream(
                self.base_path + self.resource_name + '/' + str(self._resource_id) + '/stream',
                devices_to_watch)

    def add_stream_callback(self, device, callback):
        self._api_iface._add_device_callback_for_stream(
                device,
                callback)

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
        "AlertOff", "AlertOn", "AlertsEnabled", "AutoStatus", "CustomOff", "CustomOn", "DayMask",
        "DevCat", "DeviceName", "DeviceType", "DimLevel", "EnableCustomOff", "EnableCustomOn",
        "Favorite", "Group", "HouseID", "Humidity", "InsteonID", "LEDLevel", "OffTime", "OnTime",
        "OperationFlags", "RampRate", "SubCat", "TimerEnabled", "FirmwareVersion", "Manufacturer",
        "ProductType", "User", "UserID", "AccessToken", "AccessTokenExpiration"
    )
    _properties = (
        "HouseID", "DeviceID", "DeviceName", "InsteonID", "IconID", "DeviceType", "DevCat", "SubCat",
        "AutoStatus", "CustomOn", "CustomOff", "EnableCustomOn", "EnableCustomOff", "DimLevel",
        "RampRate", "OperationFlags", "LEDLevel", "AlertsEnabled", "AlertOn", "AlertOff", "Favorite",
        "Humidity", "DayMask", "OnTime", "OffTime", "TimerEnabled", "Group", "FirmwareVersion", "LinkWithHub",
        "BeepOnPress", "LocalProgramLock", "BlinkOnTraffic", "ConfiguredGroups", "InsteonEngine", "SerialNumber",
        "Manufacturer", "ProductType", "User", "UserID", "AccessToken", "AccessTokenExpiration", "GroupList"
    )

    @property
    def DeviceCategory(self):
        import yaml
        import os
        try:
            file_dir = os.path.dirname(os.path.realpath(__file__))
            with open(file_dir+"/categories.yml", encoding='utf-8') as categories_file:
                categories = yaml.load(categories_file) or {}
        except yaml.YAMLError:
            return "No Category"
        return categories.get('dev_cat', {}).get(self.DevCat, "No Category")
