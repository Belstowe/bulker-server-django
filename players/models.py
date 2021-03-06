from asyncio import constants
import datetime
import uuid
from random import randint, choice
from django.db import models


class Player(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    def generate_age():
        return randint(16, 75)

    def generate_gender():
        return choice(('M', 'F'))

    id = models.UUIDField(verbose_name='ID', primary_key=True, db_index=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(verbose_name='Date Created', auto_now_add=True, editable=False)
    name = models.CharField(verbose_name='Name', max_length=256)
    is_alive = models.BooleanField(verbose_name='Is Alive?', default=True)
    age = models.IntegerField(verbose_name='Age', default=generate_age)
    gender = models.CharField(verbose_name='Gender', max_length=1, choices=GENDER_CHOICES, default=generate_gender)
    votedfor = models.ForeignKey('self', verbose_name='Voted for', on_delete=models.SET_NULL, related_name='votespree', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Players'
        verbose_name = 'Player'

    def is_fertile(self):
        max_fertile_age = {
            'M': 50,
            'F': 45
        }
        return self.age in range(16, max_fertile_age[self.gender])
