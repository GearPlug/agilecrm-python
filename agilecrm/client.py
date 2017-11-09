import requests
from agilecrm.exceptions import UnauthorizedError


class Client(object):
    BASE_URL = 'https://{}.agilecrm.com/dev/api/'

    def __init__(self, api_key, email, domain):
        self.api_key = api_key
        self.email = email
        self.domain = domain
        self.url = self.BASE_URL.format(self.domain)

    def create_contact(self, data):
        """Accepts contact JSON as post data along with the credentials of domain User (User name and API Key).

        Each field is case sensitive.
        Please don't pass null value.
        If you don't know value of field then either don't pass that field or pass empty data to a field.

        Args:
            data: A dict with the user's data.

        Returns:
            A dict.

        """
        return self._post('contacts', data=data)

    def get_contact_by_id(self, contact_id):
        """Returns contact object which is associated with given id

        Args:
            contact_id: A string with the user's id.

        Returns:
            A dict.

        """
        return self._get('contacts/{}'.format(contact_id))

    def get_contact_by_email(self, email):
        """Returns contact object which is associated with given email

        Args:
            email: A string with the user's email.

        Returns:
            A dict.

        """
        return self._get('contacts/search/email/{}'.format(email))

    def update_contact(self, data):
        """We can update required property fields of the contact using this call.
        It is used to add the new property or update the existing property.
        It accepts property object of contact with valid parameter in it.
        We need to send the Contact-Id of the contact to identify it.
        This will not affect other fields.

        Using this API you can not delete properties.
        If subtype is same for phone,website or email then value can be overridden.
        Lead score, star value and tags can not be updated using this API.
        follow the below API for editing lead score,star value and tags.

        Args:
            data: A dict with the user's data.

        Returns:

        """
        return self._put('contacts/edit-properties', data=data)

    def delete_contact(self, contact_id):
        """Deletes contact based on the id of the contact, which is sent in request url path.

        Args:
            contact_id: A string with the user's id.

        Returns:

        """
        return self._delete('contacts/{}'.format(contact_id))

    def dynamic_search(self, data):
        """Returns contacts or companies object which is associated with given filter

        Args:
            data: A dict with the query.

        Returns:
            A dict.

        """
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return self._post('filters/filter/dynamic-filter', data=data, headers=headers, json=False)

    def _get(self, endpoint, params=None):
        response = self._request('GET', endpoint, params=params)
        return self._parse(response)

    def _post(self, endpoint, params=None, data=None, headers=None, json=True):
        response = self._request('POST', endpoint, params=params, data=data, headers=headers, json=json)
        return self._parse(response)

    def _put(self, endpoint, params=None, data=None):
        response = self._request('PUT', endpoint, params=params, data=data)
        return self._parse(response)

    def _delete(self, endpoint, params=None):
        response = self._request('DELETE', endpoint, params=params)
        return self._parse(response)

    def _request(self, method, endpoint, params=None, data=None, headers=None, json=True):
        _headers = self._headers()
        if headers:
            _headers.update(headers)
        kwargs = {}
        if json:
            kwargs['json'] = data
        else:
            kwargs['data'] = data
        return requests.request(method, self.url + endpoint, params=params, headers=_headers,
                                auth=(self.email, self.api_key), **kwargs)

    def _parse(self, response):
        if response.status_code == 204:
            return None
        if response.status_code == 401:
            raise UnauthorizedError
        if response.headers['Content-Type'] == 'application/json':
            return response.json()

        return response.text

    def _headers(self):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
