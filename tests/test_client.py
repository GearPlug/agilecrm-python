import datetime
import os
import json
from unittest import TestCase
from agilecrm.client import Client


class OdooCRMTestCases(TestCase):
    def setUp(self):
        self.api_key = os.environ.get('API_KEY')
        self.email = os.environ.get('EMAIL')
        self.domain = os.environ.get('DOMAIN')
        self.client = Client(self.api_key, self.email, self.domain)

    def test_create_contact(self):
        contact_data = {
            "star_value": "4",
            "lead_score": "92",
            "tags": [
                "Lead",
                "Likely Buyer"
            ],
            "properties": [
                {
                    "type": "SYSTEM",
                    "name": "first_name",
                    "value": "Los "
                },
                {
                    "type": "SYSTEM",
                    "name": "last_name",
                    "value": "Bruikheilmer"
                },
                {
                    "type": "SYSTEM",
                    "name": "company",
                    "value": "steady.inc"
                },
                {
                    "type": "SYSTEM",
                    "name": "title",
                    "value": "VP Sales"
                },
                {
                    "type": "SYSTEM",
                    "name": "email",
                    "subtype": "work",
                    "value": os.environ.get('TEST_CONTACT_EMAIL')
                },
                {
                    "type": "SYSTEM",
                    "name": "address",
                    "value": "{\"address\":\"225 George Street\",\"city\":\"NSW\",\"state\":\"Sydney\",\"zip\":\"2000\",\"country\":\"Australia\"}"
                },
                {
                    "type": "CUSTOM",
                    "name": "My Custom Field",
                    "value": "Custom value"
                }
            ]
        }
        response = self.client.create_contact(contact_data)
        self.assertIsInstance(response, dict)

    def test_contact_by_id(self):
        response = self.client.get_contact_by_id(os.environ.get('TEST_CONTACT_ID'))
        self.assertIsInstance(response, dict)

    def test_contact_by_email(self):
        response = self.client.get_contact_by_email(os.environ.get('TEST_CONTACT_EMAIL'))
        self.assertIsInstance(response, dict)

    def test_update_contact(self):
        update_contact_data = {
            "id": os.environ.get('TEST_CONTACT_ID'),
            "properties": [
                {
                    "type": "SYSTEM",
                    "name": "last_name",
                    "value": "Chan"
                },
                {
                    "type": "CUSTOM",
                    "name": "My Custom Field",
                    "value": "Custom value chane"
                }
            ]
        }
        response = self.client.update_contact(update_contact_data)
        self.assertIsInstance(response, dict)

    def test_delete_contact(self):
        response = self.client.delete_contact(os.environ.get('TEST_CONTACT_ID'))
        self.assertIsInstance(response, dict)

    def test_search(self):
        today = datetime.datetime.today().timestamp()
        last_week = (datetime.datetime.today() - datetime.timedelta(days=7)).timestamp()
        my_json = {
            "rules": [{"LHS": "created_time", "CONDITION": "BETWEEN", "RHS": last_week, "RHS_NEW": today}],
            "contact_type": "PERSON"}
        response = self.client.search({
            'page_size': 25,
            'global_sort_key': '-created_time',
            'filterJson': json.dumps(my_json)
        })
        self.assertIsInstance(response, dict)
