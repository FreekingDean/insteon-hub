from urllib.parse import urlencode
import json
import sys
import requests
import time

API_URL = "https://connect.insteon.com"

class APIError(Exception):
    """API Error Response

    Attributes:
        msg -- the error message
        code -- the error code
    """
    def __init__(self, data):
        self.data = data

class InsteonAPI(object):
    def __init__(self, authorizer, client_id, user_agent):
        self.authorizer = authorizer
        self.user_agent = user_agent
        self.client_id = client_id

    def get(self, path, parameters = ''):
        '''Perform GET Request'''

        if parameters != '':
            parameter_string = ''
            for k,v in parameters.items():
                parameter_string += '{}={}'.format(k,v)
                parameter_string += '&'
            path += '?' + parameter_string

        response = requests.get(API_URL + path, headers=self._set_headers())
        return self._check_response(response)

    def post(self, path, data={}):
        '''Perform POST Request '''
        response = requests.post(API_URL + path, data=json.dumps(data), headers=self._set_headers())
        return self._check_response(response)

    def put(self, path, data={}):
        '''Perform PUT Request'''
        response = requests.put(API_URL + path, data=json.dumps(data), headers=setup_headers())
        return self._check_response(response)

    def delete(self, path, parameters={}):
        '''Perform GET Request'''

        if parameters != '':
            parameter_string = ''
            for k,v in parameters.items():
                parameter_string += '{}={}'.format(k,v)
                parameter_string += '&'
            path += '?' + parameter_string

        response = requests.delete(API_URL + path, headers=self._set_headers())
        return self._check_response(response)

    def _check_response(self, response):
        if response.status_code >= 400:
            raise APIError(response.json())

        if response.status_code == 204:
            return True

        return response.json()

    def _set_headers(self):
        return {
                "Content-Type": "application/json",
                "Authentication": "APIKey " + self.client_id,
                "Authorization": "Bearer " + self.authorizer.access_token
            }

    @classmethod
    def unauth_post(cls, path, data):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(API_URL + '/api/v2/oauth2/token', data=data, headers=headers)
        return response.json()

class InsteonResource(object):
    base_path="/api/v2/"

    def all(cls, api):
        resources = []
        try:
            response = api.get(cls.base_path + cls.resource_name, {'properties':'all'})
            for data in response[cls.resource_name[:-1].title()+"List"]:
                resources.append(cls(api, data[cls.resource_name[:-1].title()+"ID"], data))
            return resources
        except APIError as e:
            print("API error: ")
            for key,value in e.data.iteritems:
                print(str(key) + ": " + str(value))

    def __init__(self, api, resource_id=None, data=None):
        for data_key in self._properties:
            setattr(self, "_" + data_key, None)
        self._resource_id = resource_id
        self._api_iface = api
        if data:
            self._update_details(data)
        else:
            self.reload_details

    def __getattr__(self, name):
        if name in self._properties:
            return getattr(self, "_"+name)
        else:
            print(name)
            raise AttributeError

    def __setattr__(self, name, value):
        if name in self._properties:
            if name in self._settables:
                self.__dict__["_"+name] = value
            else:
                raise "Property not settable"
        else:
            self.__dict__[name] = value

    def _update_details(self, data):
        #Intakes dict of details, and sets necessary properties in device
        for api_name in self._properties:
            if api_name in data:
                setattr(self, "_" + api_name, data[api_name])

    def reload_details(self):
        #Query hub and refresh all properties
        try:
            data = self._api_iface.get(self.base_path+ self.resource_name + "/" + str(self._resource_id))
            print(data)
            self._update_details(data)
        except APIError as e:
            print("API error: ")
            for key,value in e.data.iteritems:
                print(str(key) + ": " + str(value))

    def save(self):
        data = {}
        for settable_name in self._settables:
            data[settable_name] = getattr(self, settable_name)
        try:
            return self._api_iface.put(base_path + resource_name + "/" + str(self._resource_id))
        except APIError as e:
            print("API error: ")
            for key,value in e.data.items():
                print(str(key) + ": " + str(value))

    @property
    def json(self):
        json_data = {}
        for attribute in self._properties:
            json_data[attribute] = getattr(self, "_" + attribute)
        return json.dumps(json_data)

class InsteonCommandable(InsteonResource):
    command_path = "commands"

    def send_command(self, command, level=None, wait=False):
        data = {
            'device_id': getattr(self, "DeviceID"),
            'command': command
        }
        if level:
            data['level'] = level
        try:
            command_info = self._api_iface.post(self.base_path + self.command_path, data)
            if wait:
                time.sleep(1)
                return self._api_iface.get(self.base_path + self.command_path + "/" + str(command_info['id']))
            else:
                return command_info
        except APIError as e:
            print("API error: ")
            for key,value in e.data.iteritems:
                print(str(key) + ": " + str(value))
