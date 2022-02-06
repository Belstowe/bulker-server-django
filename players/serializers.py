import uuid
from rest_framework import serializers
from .models import Player

class PlayerSerializer(serializers.ModelSerializer):
    fertile = serializers.SerializerMethodField()
    
    class Meta:
        model = Player
        fields = ('id', 'date', 'name', 'is_alive', 'age', 'gender', 'fertile')
        read_only_fields = ('id', 'date', 'fertile')
        extra_kwargs = {
            'is_alive': {
                'required': False
            },
            'age': {
                'required': False
            },
            'gender': {
                'required': False
            }
        }
        
    def get_fertile(self, obj):
        return obj.is_fertile()
        
class VotedBySerializer(serializers.ModelSerializer):
    votespree = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='id'
    )
    
    class Meta:
        model = Player
        fields = ['votespree']
        
class VotedForSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['votedfor']
        extra_kwargs = {
            'votedfor': {
                'allow_null': True
            }
        }