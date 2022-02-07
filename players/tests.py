from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
import json

# APIClient app
client = Client()


class PostPlayersTest(TestCase):
    def setUp(self):
        self.player1valid = {
            'name': 'Uno'
        }
        self.player2valid = {
            'age': 40,
            'name': 'Dos',
            'gender': 'F',
            'is_alive': False
        }
        self.player1invalid = {
            'age': 24
        }
        self.player2invalid = {
            'name': 'Tres',
            'gender': 'aa',
            'age': 20
        }

    def post_response(self, payload):
        response = client.post(
            reverse('Players:players_view'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        return response.status_code

    def test_post_player1valid(self):
        self.assertEqual(self.post_response(self.player1valid), status.HTTP_201_CREATED)

    def test_post_player2valid(self):
        self.assertEqual(self.post_response(self.player2valid), status.HTTP_201_CREATED)

    def test_post_player1invalid(self):
        self.assertEqual(self.post_response(self.player1invalid), status.HTTP_400_BAD_REQUEST)

    def test_post_player2invalid(self):
        self.assertEqual(self.post_response(self.player2invalid), status.HTTP_400_BAD_REQUEST)
