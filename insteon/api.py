from urllib.parse import urlencode
import json
import sys
import requests

API_URL = "https://connect.insteon.com"

class InsteonAPI(object):
    def __init__(self, authorizer, user_agent):
        self.authorizer = authorizer
        self.user_agent = user_agent

    def get(self, path, parameters = ''):
        '''Perform GET Request'''

        if parameters != '':
            parameter_string = ''
            for k,v in parameters.items():
                parameter_string += '{}={}'.format(k,v)
                parameter_string += '&'
            url += '?' + parameter_string

        response = requests.get(API_URL + url, headers=_set_headers()
        data = response.json()
        return _check_response(data)

    def post(self, path, data={}):
        '''Perform POST Request '''

        response = requests.post(API_URL + url, data=json.dumps(data), headers=_set_headers())
        data = response.json()
        return _check_response(data)

    def put(self, url, data={}):
        '''Perform PUT Request'''
        response = requests.put(API_URL + url, data=json.dumps(data), headers=setup_headers())
        data = response.json()
        return _check_response(data)

    def delete(self, url, parameters={}):
        '''Perform GET Request'''

        if parameters != '':
            parameter_string = ''
            for k,v in parameters.items():
                parameter_string += '{}={}'.format(k,v)
                parameter_string += '&'
            url += '?' + parameter_string

        response = requests.delete(API_URL + url, headers=_set_headers()
        data = response.json()
        return _check_response(data)

    def _check_response(self):
        if response.status_code >= 400:
            raise APIError(data)

        if response.status_code == 204:
            return True

        return response.json()

    def _setup_headers(self):
        return {
                "Content-Type": "application/json",
                "Authentication": "APIKey " + self.client_id,
                "Authorization": "Bearer " + self.authorizer.access_token
            }

    @classmethod
    def unauth_post(cls, path, data)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(API_URL + '/api/v2/oauth2/token', data=data, headers=headers)
        self.auth = response.json()
