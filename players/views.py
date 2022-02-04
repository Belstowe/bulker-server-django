from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Player
from .serializers import PlayerSerializer

class PlayersView(APIView):
    serializer_class = PlayerSerializer
    model = Player
    
    def get(self, request):
        serializer_readall = self.serializer_class(
            instance=self.model.objects.all(),
            many=True
        )
        return Response(serializer_readall.data)
    
    def post(self, request):
        serializer_write = self.serializer_class(
            data=request.data
        )
        serializer_write.is_valid(raise_exception=True)
        serializer_write.save()
        return Response(
            data=serializer_write.data,
            status=status.HTTP_201_CREATED
        )