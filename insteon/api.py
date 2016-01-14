from urllib.parse import urlencode
import json
import sys
import requests

class InsteonAPI(object):
    def __init__(self, access_token, client_id, user_agent):

    def get(self, url, parameters = ''):
        '''Perform Get Request authentication packet'''
        headers={"Content-Type": "application/json",
                "Authentication": "APIKey " + self.client_id,
                "Authorization": "Bearer " + self.authorizer.token['access_token']
        }

        if parameters != '':
            parameter_string = ''
            for k,v in parameters.items():
                parameter_string += '{}={}'.format(k,v)
                parameter_string += '&'
            url += '?' + parameter_string

        response = requests.get(API_URL + url, headers=headers)
        data = response.json()

        if response.status_code != 200:
            raise APIError(data)
        else:
            return data

    @classmethod
    def unauth_post(cls, path, data)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(API_URL + '/api/v2/oauth2/token', data=data, headers=headers)
        self.auth = response.json()
