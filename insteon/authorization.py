from urllib.parse import urlencode
import json
import sys
import requests
from .version import VERSION, API_URL

class InsteonAuthorizer(object):
    auth = None
    def __init__(self,client_id, access_token=None,
            user_agent='insteon_hub/%s' % VERSION):
        self.client_id = client_id;

    def authorize(self, username=None, password=None):
        '''Check if we have an auth and use that otherwise password login'''
        if self.auth == None:
            self._login(username, password)
        else:
            self._refresh()


    def _login(self, username, password):
        '''Login and return the JSON authentication packet'''

        data = {
            'grant_type':   'password',
            'username':     username,
            'password':     password,
            'client_id':    self.client_id
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(API_URL + '/api/v2/oauth2/token', data=data, headers=headers)
        self.auth = response.json()
        print(self.auth)

    def _refresh(self):
        '''Refresh the auth token'''

        data = {
            'grant_type':    'refresh_token',
            'refresh_token': self.auth['refresh_token'],
            'client_id':     self.client_id
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(API_URL + '/api/v2/oauth2/token', data=data, headers=headers)
        self.auth = response.json()
        print(self.auth)
