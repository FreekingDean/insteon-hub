# -*- coding:utf-8 -*-

from urllib.parse import urlencode
import json
import sys
import requests
from .authorization import InsteonAuthorizer
from .api import InsteonAPI, APIError
from .resources import House, Account, Contact, Device
from .const import __version__

class Insteon(object):
    def __init__(self, username, password, client_id,
                user_agent='insteon_hub/%s' % __version__):

        self.authorizer = InsteonAuthorizer(client_id)
        self.authorizer.authorize(username, password)
        self.api = InsteonAPI(self.authorizer, client_id, user_agent)

        # Create empty lists for objects
        self.accounts = Account.all(Account, self.api)
        self.houses = House.all(House, self.api)
        self.devices = Device.all(Device, self.api)
        #self.cameras = []
        #self.scenes = []
        #self.rooms = []
        self.contacts = Contact.all(Contact, self.api)
        #self.alerts = []
        #self.commands = []

        #self.refresh_houses()
        #self.refresh_devices()

    def refresh_devices(self):
        '''Queries hub for list of devices, and creates new device objects'''
        try:
            response = self.api.get("/api/v2/devices", {'properties':'all'})
            for device_data in response['DeviceList']:
                self.devices.append(Device(device_data, self))
        except APIError as e:
            print("API error: ")
            for key,value in e.data.iteritems:
                print(str(key) + ": " + str(value))

class DeviceP(object):
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
