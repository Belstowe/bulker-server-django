from cmath import e
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from ..serializers import PlayerSerializer
from ..models import Player
import json

# APIClient app
client = Client()


class GetPlayerTest(TestCase):
    def setUp(self):
        self.uno = Player.objects.create(name='Uno')
        self.dos = Player.objects.create(
            name='Dos', age=40, gender='F', is_alive=False)
        self.tres = Player.objects.create(
            name='Tres', age=52, gender='M')

    def test_get_player_dos(self):
        response = client.get(
            reverse('Players:player_detail', kwargs={'pk': self.dos.pk})
        )
        player = Player.objects.get(pk=self.dos.pk)
        serializer = PlayerSerializer(player)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_player(self):
        response = client.get(
            reverse('Players:player_detail', kwargs={'pk': '6b016083-77a5-4455-b318-ad70c97f2353'})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PutPlayerTest(TestCase):
    def setUp(self):
        self.uno = Player.objects.create(name='Uno')
        self.dos = Player.objects.create(
            name='Dos', age=40, gender='F', is_alive=False)
        self.tres = Player.objects.create(
            name='Tres', age=81, gender='M')

    def test_put_player_valid(self):
        response = client.put(
            reverse('Players:player_detail', kwargs={'pk': self.tres.pk}),
            data=json.dumps({'age': 18}),
            content_type='application/json'
        )
        player = Player.objects.get(pk=self.tres.pk)
        serializer = PlayerSerializer(player)
        self.assertEqual(serializer.data['is_alive'], True)
        self.assertEqual(serializer.data['age'], 18)
        self.assertEqual(serializer.data['gender'], 'M')
        self.assertEqual(serializer.data['fertile'], True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_player_invalid_gender(self):
        response = client.put(
            reverse('Players:player_detail', kwargs={'pk': self.tres.pk}),
            data=json.dumps({'gender': 'A'}),
            content_type='application/json'
        )
        player = Player.objects.get(pk=self.tres.pk)
        serializer = PlayerSerializer(player)
        self.assertEqual(serializer.data['gender'], 'M')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_player_invalid_id(self):
        response = client.put(
            reverse('Players:player_detail', kwargs={'pk': self.tres.pk}),
            data=json.dumps({'id': '6b016083-77a5-4455-b318-ad70c97f2353'}),
            content_type='application/json'
        )
        player = Player.objects.get(pk=self.tres.pk)
        serializer = PlayerSerializer(player)
        self.assertNotEqual(serializer.data['id'], '6b016083-77a5-4455-b318-ad70c97f2353')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_unknown_player(self):
        response = client.put(
            reverse('Players:player_detail', kwargs={'pk': '6b016083-77a5-4455-b318-ad70c97f2353'}),
            data=json.dumps({'age': 18}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeletePlayerTest(TestCase):
    def setUp(self):
        self.uno = Player.objects.create(name='Uno')
        self.dos = Player.objects.create(
            name='Dos', age=40, gender='F', is_alive=False)
        self.tres = Player.objects.create(
            name='Tres', age=81, gender='M')

    def test_delete_player_valid(self):
        pk_to_delete = self.dos.pk
        response = client.delete(
            reverse('Players:player_detail', kwargs={'pk': pk_to_delete})
        )
        players = Player.objects.all()
        self.assertEqual(len(players), 2)
        players = Player.objects.filter(pk=pk_to_delete)
        self.assertEqual(len(players), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_player_invalid(self):
        response = client.delete(
            reverse('Players:player_detail', kwargs={'pk': '6b016083-77a5-4455-b318-ad70c97f2353'})
        )
        players = Player.objects.all()
        self.assertEqual(len(players), 3)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
