import logging
import requests


class Client(object):
    BASE_URL = 'https://{}.agilecrm.com/dev/api/'

    def __init__(self, api_key, email, domain):
        self.api_key = api_key
        self.email = email
        self.domain = domain
        self.url = self.BASE_URL.format(self.domain)

    def create_contact(self, data):
        return self._post('contacts', data=data)

    def get_contact_by_id(self, contact_id):
        return self._get('contacts/{}'.format(contact_id))

    def get_contact_by_email(self, email):
        return self._get('contacts/search/email/{}'.format(email))

    def update_contact(self, data):
        return self._put('contacts/edit-properties', data=data)

    def delete_contact(self):
        pass

    def _get(self, endpoint, params=None):
        response = self._request('GET', endpoint, params=params)
        return self._parse(response)

    def _post(self, endpoint, params=None, data=None):
        response = self._request('POST', endpoint, params=params, data=data)
        return self._parse(response)

    def _put(self, endpoint, params=None, data=None):
        response = self._request('PUT', endpoint, params=params, data=data)
        return self._parse(response)

    def _delete(self, endpoint, params=None):
        response = self._request('DELETE', endpoint, params=params)
        return self._parse(response)

    def _request(self, method, endpoint, params=None, data=None):
        return requests.request(method, self.url + endpoint, params=params, json=data, headers=self._headers(),
                                auth=(self.email, self.api_key))

    def _parse(self, response):
        if response.status_code == 204:
            return None
        if response.headers['Content-Type'] == 'application/json':
            return response.json()

        return response.text

    def _headers(self):
        return {
            'Accept': 'application/json',
            'content-type': 'application/json',
        }
