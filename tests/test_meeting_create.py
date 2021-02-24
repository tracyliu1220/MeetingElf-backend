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

    def meeting_create(self):
        response = self.client.post('/meetings',
                                    follow_redirects=True,
                                    json={
                                        "title": "The New Weekly Meeting",
                                        "mode": "weekly",
                                        "description": "The meetings will last for about 1 hour.",
                                        "meeting_link": "https://meet.google.com/uro-dkkz-brc",
                                        "location": "EC321",
                                        "start_hour": 8,
                                        "end_hour": 21
                                    })
        self.meeting_hash_id = response.get_json()['hash_id']
        return response

    def user_meetings(self):
        response = self.client.post('/user/' + str(self.id) + '/meetings')
        return response

class CheckMeetingCreate(SettingBase):
    def test_meeting_create(self):
        response = self.signup()
        response = self.login()
        response = self.meeting_create()
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    # unittest.main()
    pass
