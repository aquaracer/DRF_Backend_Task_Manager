import os

from rest_framework import status
import unittest, requests
from django.contrib.auth.models import User


class TestBasic(unittest.TestCase):

    def get_json(self, **kwargs):
        response = requests.post(**kwargs)
        return response.json()

    def setUp(self):
        self.domain = 'http://127.0.0.1:8000'
        self.create_user_url = f'{self.domain}/auth/users/'
        self.login_url = f'{self.domain}/auth/token/login/'
        self.task_list_url = f'{self.domain}/api/tasks/'
        self.filtered_task_list_url = f'{self.domain}/api/filtered_tasks/'
        self.task_changes_list_url = f'{self.domain}/api/task_changes/'
        self.credentials = os.getenv('TEST_CREDENTIALS')
        token = self.get_json(url=self.login_url, json=self.credentials)
        self.token = token['auth_token']

    def test_obtain_token(self):
        response = requests.post(url=self.login_url, json=self.credentials)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_obtain_token_negaive(self):
        cases = [
            ({},
             {"non_field_errors": ["Unable to log in with provided credentials."]}),

            ({
                 "username": "",
                 "password": "",
             },
             {
                 "username": ["This field may not be blank."],
                 "password": ["This field may not be blank."]
             }),
            ({
                 "username": "admin",
                 "password": "123",

             },
             {
                 "non_field_errors": [
                     "Unable to log in with provided credentials."
                 ]
             }
            ),
        ]

        for сredentials, expected in cases:
            with self.subTest():
                self.assertEqual(self.get_json(url=self.login_url, json=сredentials), expected)

    def test_create_user(self):
        data = {
            "username": "user@mail.ru",
            "password": "WFWdc213$&ZZv12xcz",
            "email": "user@mail.ru"
        }
        response = requests.post(url=self.create_user_url, json=data)
        User.objects.filter(username=data['username']).delete()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_negative(self):
        cases = [
            ({},
             {"username": ["This field is required."],
              "password": ["This field is required."]
              }),

            ({"username": "userwdwd",
              "password": "123",
              "email": "user@mail.ru"
              },
             {
                 "password": [
                     "This password is too short. It must contain at least 8 characters.",
                     "This password is too common.",
                     "This password is entirely numeric."]}
             ),
            ({"username": "user287690",
              "password": "WFWdc213$&ZZv12",
              "email": "user"},
             {
                 "email": [
                     "Enter a valid email address."
                 ]
             })]

        for data, expected in cases:
            with self.subTest():
                self.assertEqual(self.get_json(url=self.create_user_url, json=data), expected)

    def test_get_task_list(self):
        response = requests.get(url=self.task_list_url, headers={'Authorization': f'Token {self.token}'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_task(self):
        data = {
            "name": "132423",
            "description": "WFWdc213$&ZZv12xcz",
            "status": "new",
            "planned_finish": "2020-10-05",
        }
        response = requests.post(url=self.task_list_url, json=data, headers={'Authorization': f'Token {self.token}'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_task_negative(self):

        cases = [

            ({
                 "name": "132423",
                 "description": "WFWdc213$&ZZv12xcz",
                 "status": "new",
                 "planned_finish": "2020-10-05",
             },
             '123',
             {
                 "detail": "Invalid token."
             }),
            ({
                 "name": "132423",
                 "description": "WFWdc213$&ZZv12xcz",
                 "status": "news",
                 "planned_finish": "2020-10-32",
             },
             self.token,
             {
                 "status": [
                     "\"news\" is not a valid choice."
                 ],
                 "planned_finish": [
                     "Date has wrong format. Use one of these formats instead: YYYY-MM-DD."
                 ]
             })]

        for data, token, expected in cases:
            with self.subTest():
                self.assertEqual(self.get_json(url=self.task_list_url,
                                               json=data,
                                               headers={'Authorization': f'Token {token}'}),
                                 expected)

    def test_update_task(self):
        data = {
            "name": "132423",
            "description": "WFWdc213$&ZZv12xcz",
            "status": "new",
            "planned_finish": "2020-10-12",
        }
        response = requests.put(url=f'{self.task_list_url}3/',
                                json=data,
                                headers={'Authorization': f'Token {self.token}'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_task_negative(self):

        cases = [

            (f'{self.task_list_url}3/',
             '123',
             {"name": "132423",
              "description": "WFWdc213$&ZZv12xcz",
              "status": "new",
              "planned_finish": "2020-10-12"},
             {
                 "detail": "Invalid token."
             }),
            (f'{self.task_list_url}122/',
             self.token,
             {"name": "132423",
              "description": "WFWdc213$&ZZv12xcz",
              "status": "new",
              "planned_finish": "2020-10-12"},
             {
                 "detail": "Not found."
             }),
            (f'{self.task_list_url}3/',
             self.token,
             {"name": "132423",
              "description": "WFWdc213$&ZZv12xcz",
              "status": "news",
              "planned_finish": "2020-10-32"},
             {
                 "status": [
                     "\"news\" is not a valid choice."
                 ],
                 "planned_finish": [
                     "Date has wrong format. Use one of these formats instead: YYYY-MM-DD."
                 ]
             }
             )]

        for url, token, data, expected in cases:
            with self.subTest():
                response = requests.put(url=url, data=data,
                                        headers={'Authorization': f'Token {token}'})
                response = response.json()
                self.assertEqual(response, expected)

    def test_get_task_list_negative(self):
        response = requests.get(url=self.task_list_url, headers={'Authorization': 'Token 123'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_filtered_task_list(self):
        response = requests.get(url=f'{self.filtered_task_list_url}new/2020-10-05/',
                                headers={'Authorization': f'Token {self.token}'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_filtered_task_list_negative(self):
        cases = [
            (f'{self.filtered_task_list_url}new/2020-10-05/',
             '123',
             {
                 "detail": "Invalid token."
             }),
            (f'{self.filtered_task_list_url}news/2020-32-05/',
             self.token,
             {"status": ["\"news\" is not a valid choice."],
              "planned_finish": ["Date has wrong format. Use one of these formats instead: YYYY-MM-DD."]
              })]

        for url, token, expected in cases:
            with self.subTest():
                response = requests.get(url=url,
                                        headers={'Authorization': f'Token {token}'})
                response = response.json()
                self.assertEqual(response, expected)

    def test_get_task_changes_list(self):
        response = requests.get(url=f'{self.task_changes_list_url}2/', headers={'Authorization': f'Token {self.token}'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_task_changes_list_negative(self):
        cases = [

            (f'{self.task_changes_list_url}2/',
             '123',
             {
                 "detail": "Invalid token."
             }),
            (f'{self.task_changes_list_url}122/',
             self.token,
             {
                 "detail": "Not found."
             })]

        for url, token, expected in cases:
            with self.subTest():
                response = requests.get(url=url,
                                        headers={'Authorization': f'Token {token}'})
                response = response.json()
                self.assertEqual(response, expected)
