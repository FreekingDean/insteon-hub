from urllib.parse import urlencode
from threading import Lock
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
        self._stream_device_callbacks = {}
        self._lock = Lock()

    def get(self, path, data=''):
        '''Perform GET Request'''
        if len(data) != 0:
            parameter_string = ''
            for k,v in data.items():
                parameter_string += '{}={}'.format(k,v)
                parameter_string += '&'
            path += '?' + parameter_string
        response = requests.get(API_URL + path, headers=self._set_headers())
        return self._check_response(response, self.get, path, data)

    def post(self, path, data={}):
        '''Perform POST Request '''
        response = requests.post(API_URL + path, data=json.dumps(data), headers=self._set_headers())
        return self._check_response(response, self.post, path, data)

    def put(self, path, data={}):
        '''Perform PUT Request'''
        response = requests.put(API_URL + path, data=json.dumps(data), headers=self._set_headers())
        return self._check_response(response, self.put, path, data)

    def delete(self, path, data={}):
        '''Perform DELETE Request'''
        if len(data) != 0:
            parameter_string = ''
            for k,v in data.items():
                parameter_string += '{}={}'.format(k,v)
                parameter_string += '&'
            path += '?' + parameter_string

        response = requests.delete(API_URL + path, headers=self._set_headers())
        return self._check_response(response, self.delete, path, data)

    def stream(self, path, devices_to_watch={}):
        headers = self._set_headers()
        headers['Content-Type'] = 'text/event-stream'
        response = None
        try:
            while True:
                response = requests.get(API_URL + path, headers = headers, stream=True)
                for line in response.iter_lines():
                    # filter out keep-alive new lines
                    if line:
                        decoded_line = line.decode('utf-8')
                        payload = decoded_line.split(': ')
                        self._handle_stream_message(payload[0], payload[1], devices_to_watch)
        except Exception as e:
            print(e)
            if response != None:
                response.connection.close()

    def _add_device_callback_for_stream(self, device, callback):
        self._lock.acquire()
        try:
            self._stream_device_callbacks[device.DeviceID] = callback
        finally:
            self._lock.release()

    def _handle_stream_message(self, message_type, payload, devices_to_watch):
        self.stream_message_mappings[message_type](self, payload, devices_to_watch)

    def _set_stream_event(self, event_name, *_):
        self._current_stream_event = event_name

    def _handle_stream_data(self, data, devices_to_watch):
        parsed_data = json.loads(data)
        changed_device = next([x for x in devices_to_watch if x.InsteonID == parsed_data['device_insteon_id']].__iter__(), None)
        if changed_device != None:
            changed_device.set_status(parsed_data['status'])
            self._lock.acquire()
            try:
                if changed_device.DeviceID in self._stream_device_callbacks:
                    self._stream_device_callbacks[changed_device.DeviceID](parsed_data['status'])
            finally:
                self._lock.release()

    stream_message_mappings = {'event': _set_stream_event, 'data': _handle_stream_data}

    def _check_response(self, response, calling_method, path, data={}):
        if response.status_code >= 400:
            if response.status_code == 401 and response.json()['code'] == 4012:
                self.authorizer.authorize()
                calling_method(path, data)
            else:
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
        self._cached_status = None
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
            return self._api_iface.put(self.base_path + self.resource_name + "/" + str(self._resource_id), data=data)
        except APIError as e:
            print("API error: ")
            for key,value in e.data.items():
                print(str(key) + ": " + str(value))

    def set_status(self, status):
        self._cached_status = status

    @property
    def status(self):
        return self._cached_status

    @property
    def json(self):
        json_data = {}
        for attribute in self._properties:
            json_data[attribute] = getattr(self, "_" + attribute)
        return json.dumps(json_data)

class InsteonCommandable(InsteonResource):
    command_path = "commands"

    def send_command(self, command, payload=None, level=None, wait=False):
        data = {
            'device_id': getattr(self, "DeviceID"),
            'command': command
        }

        if command in ['on', 'off', 'fast_on', 'fast_off']:
            self.set_status(command)

        if payload:
            for key in payload:
                data[key] = payload[key]

        if level:
            data['level'] = level

        try:
            command_info = self._api_iface.post(self.base_path + self.command_path, data)
            if wait:
                commandId = command_info['id']
                commandStatus = command_info['status']
                while commandStatus == 'pending':
                    time.sleep(0.4)
                    command_info = self._api_iface.get(self.base_path + self.command_path + "/" + str(commandId))
                    commandStatus = command_info['status']
            return command_info
        except APIError as e:
            print("API error: executing command " + str(command) + " on " + self.DeviceName)
            print(vars(e))
