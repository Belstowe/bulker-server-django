from asyncio import constants
import uuid
from django.db import models

class Player(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    id = models.UUIDField(verbose_name='ID', primary_key=True, db_index=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(verbose_name='Date Created', editable=False)
    name = models.CharField(verbose_name='Name', max_length=256)
    age = models.IntegerField(verbose_name='Age')
    gender = models.CharField(verbose_name='Gender', max_length=1, choices=GENDER_CHOICES, default='M')
    
    class Meta:
        verbose_name_plural = 'Players'
        verbose_name = 'Player'

    def is_fertile(self):
        return self.age in range(16, 45)