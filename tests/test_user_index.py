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

    def user_index(self):
        response = self.client.get('/users',
                                    follow_redirects=True)
        return response

class CheckUserShow(SettingBase):
    def test_user_index(self):
        response = self.signup()
        response = self.user_index()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

if __name__ == '__main__':
    unittest.main()
