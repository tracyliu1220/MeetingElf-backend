import unittest
from flask import url_for
from flask_testing import TestCase
from app import app, db
import json

class SettingBase(TestCase):
    def create_app(self):
        return app

    def setUp(self):
        db.create_all()
        self.username = "test"
        self.email = "test@example.com"
        self.password = "1234"
        self.id = -1

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def signup(self):
        response = self.client.post('/users',
                                    follow_redirects=True,
                                    json={
                                        "username": self.username,
                                        "email": self.email,
                                        "password": self.password
                                    })
        return response

    def login(self):
        response = self.client.post('/auth/login',
                                    follow_redirects=True,
                                    json={
                                        "email": self.email,
                                        "password": self.password
                                    })
        self.id = response.get_json()['id']
        return response

    def user_show(self):
        response = self.client.get('/users/' + str(self.id),
                                    follow_redirects=True)
        return response

class CheckUserShow(SettingBase):
    def test_user_show(self):
        response = self.signup()
        response = self.login()
        response = self.user_show()
        self.assertEqual(response.status_code, 200)
    
    def test_user_show_401(self):
        response = self.signup()
        response = self.user_show()
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
