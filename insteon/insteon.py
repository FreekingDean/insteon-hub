# -*- coding:utf-8 -*-

from urllib.parse import urlencode
import json
import sys
import requests
from .authorization import InsteonAuthorizer

class APIError(Exception):
    """API Error Response

    Attributes:
        msg -- the error message
        code -- the error code
    """
    def __init__(self, data):
        self.data = data

class Insteon(object):
    def __init__(self, username, password, client_id,
                access_token=None, user_agent='LibPyInsteon/0.1'):

        self.client_id = client_id;
        self.authorizer = InsteonAuthorizer(client_id)
        self.authorizer.authorize(username, password)

        # Create empty lists for objects
        self.accounts = []
        self.houses = []
        self.devices = []
        self.cameras = []
        self.scenes = []
        self.rooms = []
        self.contacts = []
        self.alerts = []
        self.commands = []

        self.refresh_houses()
        self.refresh_devices()

    def refresh_houses(self):
        '''Queries hub for list of houses, and creates new house objects'''
        try:
            response = self._api_get("/api/v2/houses", {'properties':'all'})
            for house_data in response['HouseList']:
                self.houses.append(House(house_data, self))
        except APIError as e:
            print("API error: ")
            for key,value in e.data.iteritems:
                print(str(key) + ": " + str(value))

    def refresh_devices(self):
        '''Queries hub for list of devices, and creates new device objects'''
        try:
            response = self._api_get("/api/v2/devices", {'properties':'all'})
            for device_data in response['DeviceList']:
                self.devices.append(Device(device_data, self))
        except APIError as e:
            print("API error: ")
            for key,value in e.data.iteritems:
                print(str(key) + ": " + str(value))

    def create_house(self):
        pass

class Account(object):
    pass

class House(object):
    def __init__(self, data, api_iface):
        self.api_iface = api_iface
        self._properties = (
            'InsteonHubID','HouseName','City','DHCP','DaylightSavings',
            'HubType','HubUsername','HubPassword','IP','Port','Gateway',
            'Mask','Mac','BinVer','PLMVer','FirmwareVer','HouseID','IconID'
        )
        self._update_details(data)

    def refresh_details(self):
        '''Query hub and refresh all properties of a house'''
        try:
            data = self.api_iface._api_get("/api/v2/houses/" + str(self.HouseID))
            print(data)
            self._update_details(data)
        except APIError as e:
            print("API error: ")
            for key,value in e.data.iteritems:
                print(str(key) + ": " + str(value))

    def _update_details(self,data):
        '''Intakes dict of details, and sets necessary properties
        in device'''
        for api_name in self._properties:
            if api_name in data:
                setattr(self, "_" + api_name, data[api_name])
            # Use setter if exists, else set variable
            # Not sure if we want this, how do we distinguish 
            # initialize versus set
            #try:
            #    getattr(House, api_name).__set__(self, data[api_name])
            #except AttributeError:
            #    setattr(self, "_" + api_name, data[api_name])
    
    @property
    def json(self):
        json_data = {}
        for attribute in self._properties:
            json_data[attribute] = getattr(self, "_" + attribute)
        return json.dumps(json_data)

    def _update_house(self):
        data = { 'InsteonHubID'   : self.InsteonHubID,
                 'HouseName'      : self.HouseName,
                 'City'           : self.City,
                 'DHCP'           : self.DHCP,
                 'DaylightSavings': self.DaylightSavings
        }
        url = "/api/v2/houses/" + str(self.HouseID)
        try:
            response = self.api_iface._api_put(url, data)
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

class Device(object):
    def __init__(self, data, api_iface):
        self.api_iface = api_iface
        self._update_details(data)

    def refresh_details(self):
        '''Query hub and refresh all details of a device,
        but NOT status, includes grouplist not present in
        refresh_all_devices'''
        try:
            return self.api_iface._api_get("/api/v2/devices/" + str(self.device_id))
        except APIError as e:
            print("API error: ")
            for key,value in e.data.iteritems:
                print(str(key) + ": " + str(value))

    def send_command(self, command):
        '''Send a command to a device'''
        data = {"command": command, "device_id": self.device_id}
        try:
            response = self.api_iface._api_post("/api/v2/commands", data)
            return Command(response, self)
        except APIError as e:
            print("API error: ")
            for key,value in e.data.iteritems:
                print(str(key) + ": " + str(value))

    def _update_details(self,data):
        '''Intakes dict of details, and sets necessary properties
        in device'''
        # DeviceName, IconID, HouseID, DeviceID always present
        self.device_id = data['DeviceID']
        self.device_name = data['DeviceName']
        self.properties = data

class Camera(object):
    pass

class Scene(object):
    pass

class Room(object):
    pass

class Contact(object):
    pass

class Alert(object):
    pass

class Command(object):
    def __init__(self, data, device):
        self.api_iface = device.api_iface
        self.device = device
        self._properties = (
            'link','status','command','response','id'
        )
        self._update_details(data)

    def _update_details(self,data):
        '''Intakes dict of details, and sets necessary properties
        in command'''
        for api_name in self._properties:
            if api_name in data:
                setattr(self, "_" + api_name, data[api_name])
            else:
                # Only set to blank if not initialized
                try:
                    getattr(self, "_" + api_name)
                except AttributeError:
                    setattr(self, "_" + api_name, '')

    def query_status(self):
        '''Query the hub for the status of this command'''
        try:
            data = self.api_iface._api_get(self.link)
            self._update_details(data)
        except APIError as e:
            print("API error: ")
            for key,value in e.data.iteritems:
                print(str(key) + ": " + str(value))

    @property
    def json(self):
        json_data = {}
        for attribute in self._properties:
            json_data[attribute] = getattr(self, "_" + attribute)
        return json.dumps(json_data)

    @property
    def link(self):
        return self._link

    @property
    def status(self):
        return self._status

    @property
    def command(self):
        return self._command

    @property
    def response(self):
        return self._response

    @property
    def id(self):
        return self._id
