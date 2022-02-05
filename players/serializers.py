import uuid
from rest_framework import serializers
from .models import Player

class PlayerSerializer(serializers.ModelSerializer):
    #name = serializers.CharField(max_length=256)
    #age = serializers.IntegerField()
    #gender = serializers.CharField(max_length=1)
    
    class Meta:
        model = Player
        fields = ('id', 'date', 'name', 'age', 'gender')
        read_only_fields = ('id', 'date')
        extra_kwargs = {
            'age': {
                'required': False
            },
            'gender': {
                'required': False
            }
        }