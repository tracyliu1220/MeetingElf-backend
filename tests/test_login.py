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
        return response

class CheckUserLogin(SettingBase):
    def test_login(self):
        response = self.signup()
        response = self.login()
        self.assertEqual(response.status_code, 200)

    def test_login_401(self):
        response = self.signup()
        self.email = 'test400@example.com'
        response = self.login()
        self.assertEqual(response.status_code, 401)
    
    def test_login_403(self):
        response = self.signup()
        self.password = '123'
        response = self.login()
        self.assertEqual(response.status_code, 403)

if __name__ == '__main__':
    unittest.main()
