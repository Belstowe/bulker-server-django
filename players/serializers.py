import uuid
from rest_framework import serializers
from .models import Player

class PlayerSerializer(serializers.ModelSerializer):
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
        
class GotVotedSerializer(serializers.ModelSerializer):
    votespree = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='id'
    )
    
    class Meta:
        model = Player
        fields = ['votespree']
        
class VotedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['votedfor']
        extra_kwargs = {
            'votedfor': {
                'allow_null': True
            }
        }