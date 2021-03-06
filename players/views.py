from django.forms import JSONField
from django.shortcuts import render
from django.http.response import JsonResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import json
from .models import Player
from .serializers import PlayerSerializer, VotedForSerializer, VotedBySerializer


class PlayersView(APIView):
    serializer_class = PlayerSerializer
    model = Player

    def get(self, request):
        serializer_readall = self.serializer_class(
            instance=self.model.objects.all(),
            many=True
        )
        return Response(
            serializer_readall.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer_write = self.serializer_class(data=request.data)
        serializer_write.is_valid(raise_exception=True)
        serializer_write.save()
        return Response(
            data=serializer_write.data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request):
        self.model.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlayerDetail(APIView):
    serializer_class = PlayerSerializer
    model = Player

    def get(self, request, pk):
        try:
            record = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return JsonResponse(
                {'message': f"Couldn't find a player record by id {pk}"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer_read = self.serializer_class(record)
        return Response(
            serializer_read.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):
        try:
            record = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return JsonResponse(
                {'message': f"Couldn't find a player record by id {pk}"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer_update = self.serializer_class(record, data=request.data, partial=True)
        if serializer_update.is_valid():
            serializer_update.save()
            return Response(
                serializer_update.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer_update.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        try:
            record = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return JsonResponse(
                {'message': f"Couldn't find a player record by id {pk}"},
                status=status.HTTP_404_NOT_FOUND
            )
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlayerVotedBy(APIView):
    subject_serializer, object_serializer = VotedForSerializer, VotedBySerializer
    model = Player

    def get(self, request, pk):
        try:
            record = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return JsonResponse(
                {'message': f"Couldn't find a player record by id {pk}"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer_get = self.object_serializer(record)
        return Response(
            serializer_get.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        player_list = self.model.objects.filter(votedfor=pk)
        for player in player_list:
            serializer_clear = self.subject_serializer(
                player,
                data={'votedfor': None}
            )
            if not serializer_clear.is_valid():
                return Response(
                    serializer_clear.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer_clear.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class PlayerVotedFor(APIView):
    subject_serializer, object_serializer = VotedForSerializer, VotedBySerializer
    model = Player

    def get(self, request, pk):
        try:
            record = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return JsonResponse(
                {'message': f"Couldn't find a player record by id {pk}"},
                status=status.HTTP_404_NOT_FOUND
            )
        object_record = record.votedfor

        if object_record is None:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer_get = PlayerSerializer(object_record)
        return Response(
            serializer_get.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        try:
            subject_record = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return JsonResponse(
                {'message': f"Couldn't find a player record by id {pk}"},
                status=status.HTTP_404_NOT_FOUND
            )
        object_record = subject_record.votedfor

        if object_record is None:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer_clear = self.subject_serializer(
            subject_record,
            data={'votedfor': None}
        )
        if not serializer_clear.is_valid():
            return Response(
                serializer_clear.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer_clear.save()

        serializer_get = self.object_serializer(object_record)
        return Response(
            serializer_get.data,
            status=status.HTTP_200_OK
        )


class PlayerVoteFor(APIView):
    subject_serializer, object_serializer = VotedForSerializer, VotedBySerializer
    model = Player

    def put(self, request, subjpk, objpk):
        try:
            subject_record = self.model.objects.get(pk=subjpk)
        except self.model.DoesNotExist:
            return JsonResponse(
                {'message': f"Couldn't find a player record by id {subjpk}"},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            object_record = self.model.objects.get(pk=objpk)
        except self.model.DoesNotExist:
            return JsonResponse(
                {'message': f"Couldn't find a player record by id {objpk}"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer_change = self.subject_serializer(
            subject_record,
            data={'votedfor': objpk}
        )
        if not serializer_change.is_valid():
            return Response(
                serializer_change.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer_change.save()

        serializer_get = self.object_serializer(object_record)
        return Response(
            serializer_get.data,
            status=status.HTTP_200_OK
        )


class AllVoted(APIView):
    model = Player

    def get(self, request):
        return Response(
            len(self.model.objects.filter(votedfor=None)) == 0,
            status=status.HTTP_200_OK
        )


class ClearVotes(APIView):
    model = Player

    def delete(self, request):
        player_list = self.model.objects.filter(votedfor__isnull=False)

        for player in player_list:
            serializer_clear = VotedForSerializer(
                player,
                data={'votedfor': None}
            )
            if not serializer_clear.is_valid():
                return Response(
                    serializer_clear.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer_clear.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
