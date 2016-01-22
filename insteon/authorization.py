from urllib.parse import urlencode
import json
import sys
import requests
import time
from .api import InsteonAPI

class InsteonAuthorizer(object):
    access_token=None
    def __init__(self, client_id):
        self.client_id = client_id

    def authorize(self, username=None, password=None):
        #Check if we have an auth and use that otherwise password login
        if self.access_token== None:
            self._login(username, password)
        else:
            self._refresh()


    def _login(self, username, password):
        #Login and return the JSON authentication packet

        response = InsteonAPI.unauth_post('/api/v2/oauth2/token', {
            'grant_type':   'password',
            'username':     username,
            'password':     password,
            'client_id':    self.client_id
        })
        self._set_auth(response)

    def _refresh(self):
        #Refresh the auth token

        response = InsteonAPI.unauth_post('/api/v2/oauth2/token', {
            'grant_type':    'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id':     self.client_id
        })
        self._set_auth(response)

    def _set_auth(self, auth_response):
        self.access_token   = auth_response['access_token']
        self.refresh_token  = auth_response['refresh_token']
        self.expiry         = auth_response['expires_in']*60 #convert to seconds to use epoch seconds
        self.last_auth      = time.time()
