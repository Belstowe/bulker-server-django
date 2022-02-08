from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from ..serializers import PlayerSerializer
from ..models import Player
import json

# APIClient app
client = Client()


class PlayerVotedByTest(TestCase):
    def setUp(self):
        self.uno = Player.objects.create(name='Uno')
        self.dos = Player.objects.create(
            name='Dos', age=40, gender='F', is_alive=False)
        self.tres = Player.objects.create(
            name='Tres', age=81, gender='M')
        self.quatro = Player.objects.create(name='Quatro')

        self.uno.votedfor = self.dos
        self.dos.votedfor = self.uno
        self.tres.votedfor = self.uno

        self.uno.save()
        self.dos.save()
        self.tres.save()

    def test_votedby_get_valid(self):
        response = {}
        for key, value in {
            'uno': self.uno.pk,
            'dos': self.dos.pk,
            'tres': self.tres.pk,
            'quatro': self.quatro.pk
        }.items():
            response[key] = client.get(
                reverse('Players:player_voted_by', kwargs={'pk': value})
            )
            self.assertEqual(response[key].status_code, status.HTTP_200_OK)

        self.assertEqual(len(response['uno'].data['votespree']), 2)
        self.assertTrue(self.dos.pk in response['uno'].data['votespree'])
        self.assertTrue(self.tres.pk in response['uno'].data['votespree'])
        self.assertEqual(len(response['dos'].data['votespree']), 1)
        self.assertTrue(self.uno.pk in response['dos'].data['votespree'])
        self.assertEqual(len(response['tres'].data['votespree']), 0)
        self.assertEqual(len(response['quatro'].data['votespree']), 0)

    def test_votedby_get_invalid(self):
        response = client.get(
            reverse('Players:player_voted_by', kwargs={'pk': '6b016083-77a5-4455-b318-ad70c97f2353'})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_votedby_delete_valid(self):
        response_uno = client.delete(
            reverse('Players:player_voted_by', kwargs={'pk': self.uno.pk})
        )
        self.assertEqual(response_uno.status_code, status.HTTP_204_NO_CONTENT)
        response_quatro = client.delete(
            reverse('Players:player_voted_by', kwargs={'pk': self.quatro.pk})
        )
        self.assertEqual(response_quatro.status_code, status.HTTP_204_NO_CONTENT)

        response = {}
        for key, value in {
            'uno': self.uno.pk,
            'dos': self.dos.pk,
            'tres': self.tres.pk,
            'quatro': self.quatro.pk
        }.items():
            response[key] = client.get(
                reverse('Players:player_voted_by', kwargs={'pk': value})
            )
            self.assertEqual(response[key].status_code, status.HTTP_200_OK)
        self.assertEqual(len(response['uno'].data['votespree']), 0)
        self.assertEqual(len(response['dos'].data['votespree']), 1)
        self.assertTrue(self.uno.pk in response['dos'].data['votespree'])
        self.assertEqual(len(response['tres'].data['votespree']), 0)
        self.assertEqual(len(response['quatro'].data['votespree']), 0)

    def test_votedby_delete_invalid(self):  # The logic behind this service doesn't require Player {id} to exist, so it still reports as success
        response = client.delete(
            reverse('Players:player_voted_by', kwargs={'pk': '6b016083-77a5-4455-b318-ad70c97f2353'})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
