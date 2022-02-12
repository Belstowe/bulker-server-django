from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from ..serializers import PlayerSerializer
from ..models import Player
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
        self.player1invalid = {  # Required field 'name' not specified
            'age': 24
        }
        self.player2invalid = {  # Illegal value in field 'gender'
            'name': 'Tres',
            'gender': 'aa',
            'age': 20
        }
        self.player3invalid = {  # Trying to assign value to read-only field 'id'
            'id': '6b016083-77a5-4455-b318-ad70c97f2353',
            'name': 'Quatro',
        }

    def post_response_code(self, payload):
        response = client.post(
            reverse('Players:players_view'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        return response.status_code

    def test_post_player1valid(self):
        self.assertEqual(self.post_response_code(self.player1valid), status.HTTP_201_CREATED)

    def test_post_player2valid(self):
        response = client.post(
            reverse('Players:players_view'),
            data=json.dumps(self.player2valid),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['age'], self.player2valid['age'])
        self.assertEqual(response.data['name'], self.player2valid['name'])
        self.assertEqual(response.data['gender'], self.player2valid['gender'])
        self.assertEqual(response.data['is_alive'], self.player2valid['is_alive'])

    def test_post_player1invalid(self):
        self.assertEqual(self.post_response_code(self.player1invalid), status.HTTP_400_BAD_REQUEST)

    def test_post_player2invalid(self):
        self.assertEqual(self.post_response_code(self.player2invalid), status.HTTP_400_BAD_REQUEST)

    def test_post_player3invalid(self):
        response = client.post(
            reverse('Players:players_view'),
            data=json.dumps(self.player3invalid),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data['id'], self.player3invalid['id'])


class GetPlayersTest(TestCase):
    def setUp(self):
        Player.objects.create(name='Uno')
        Player.objects.create(
            name='Dos', age=40, gender='F', is_alive=False)

    def test_get_players(self):
        response = client.get(reverse('Players:players_view'))
        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeletePlayersTest(TestCase):
    def setUp(self):
        Player.objects.create(name='Uno')
        Player.objects.create(name='Dos')

    def test_delete_players(self):
        response = client.delete(reverse('Players:players_view'))
        players = Player.objects.all()
        self.assertEqual(len(players), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
