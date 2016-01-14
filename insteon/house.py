from .api import InsteonResource

class House(InsteonResource):
    resource_name="houses"
    def __init__(self, data):
        self._properties = (
            'InsteonHubID','HouseName','City','DHCP','DaylightSavings',
            'HubType','HubUsername','HubPassword','IP','Port','Gateway',
            'Mask','Mac','BinVer','PLMVer','FirmwareVer','HouseID','IconID'
        )
        self._update_details(data)


    def _update_house(self):
        data = { 'InsteonHubID'   : self.InsteonHubID,
                 'HouseName'      : self.HouseName,
                 'City'           : self.City,
                 'DHCP'           : self.DHCP,
                 'DaylightSavings': self.DaylightSavings
        }
        path = "/api/v2/houses/" + str(self.HouseID)
        try:
            response = self.api_iface.put(url, data)
            return response
        except APIError as e:
            print("API error: ")
            for key,value in e.data.items():
                print(str(key) + ": " + str(value))

    @property
    def HouseName(self):
        return self._HouseName

    @HouseName.setter
    def HouseName(self, value):
        self._HouseName = value
        self._update_house()

    @property
    def InsteonHubID(self):
        return self._InsteonHubID

    @property
    def City(self):
        return self._City

    @City.setter
    def City(self, value):
        self._City = value
        self._update_house()

    @property
    def DHCP(self):
        return self._DHCP

    @DHCP.setter
    def DHCP(self, value):
        self._DHCP = value
        self._update_house()

    @property
    def DaylightSavings(self):
        return self._DaylightSavings

    @DaylightSavings.setter
    def DaylightSavings(self, value):
        self._DaylightSavings = value
        self._update_house()

    @property
    def HubType(self):
        return self._HubType

    @property
    def HubUsername(self):
        return self._HubUsername

    @property
    def HubPassword(self):
        return self._HubPassword

    @property
    def IP(self):
        return self._IP

    @property
    def Port(self):
        return self._Port

    @property
    def Gateway(self):
        return self._Gateway

    @property
    def Mask(self):
        return self._Mask

    @property
    def Mac(self):
        return self._Mac

    @property
    def BinVer(self):
        return self._BinVer

    @property
    def PLMVery(self):
        return self._PLMVery

    @property
    def FirmwareVer(self):
        return self._FirmwareVer

    @property
    def HouseID(self):
        return self._HouseID

    @property
    def IconID(self):
        return self._IconID

    def delete(self):
        pass
