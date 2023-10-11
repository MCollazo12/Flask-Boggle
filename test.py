from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle
import json


class FlaskTests(TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True

    def test_make_board(self):
        with self.client:
            response = self.client.get("/")

            self.assertEqual(response.status_code, 200)
            self.assertIn("board", session)
            self.assertIsNone(session.get("guesses"))
            self.assertIsNone(session.get("num_plays"))
            self.assertIsNone(session.get("highscore"))
            self.assertIsNone(session.get("num_plays"))

    def test_check_guess(self):
        with self.client as client:
            with client.session_transaction() as session:
                session["board"] = [
                    ["A", "B", "C", "D", "E"],
                    ["F", "G", "H", "I", "J"],
                    ["K", "L", "M", "N", "O"],
                    ["P", "Q", "R", "S", "T"],
                    ["U", "V", "W", "X", "Y"],
                ]
        response = self.client.get("/check-guess?guess=jot")

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["result"], "ok")

    def test_invalid_guess(self):
        self.client.get('/')
        response = self.client.get('/check-guess?guess=dog')
        data = response.get_json()
        self.assertEqual(data["result"], 'not-on-board')
        
    def test_not_word(self):
        self.client.get('/')
        response = self.client.get('/check-guess?guess=bwojndsoj')
        data = response.get_json()
        self.assertEqual(data["result"], 'not-a-word')
        
    def test_show_score(self):
        with self.client:
            data = {'score': 10}
            response = self.client.post('/show-score', json=data)
            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.get_data(as_text=True))
            self.assertEqual(response_data['newrecord'], True)