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

class CheckUserSignUp(SettingBase):
    def test_signup(self):
        response = self.signup()
        self.assertEqual(response.status_code, 200)

    # signup 2 times
    def test_signup_400(self):
        response = self.signup()
        response = self.signup()
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
