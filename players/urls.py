from django.urls import path, include
from .views import *

app_name = 'Players'
urlpatterns = [
    path(
        'Players',
        PlayersView.as_view(),
        name='players_view'
    ),
    path(
        'Players/<uuid:pk>',
        PlayerDetail.as_view(),
        name='player_detail'
    ),
    path(
        'Players/<uuid:pk>/Vote',
        PlayerVotedFor.as_view(),
        name='player_voted_for'
    ),
    path(
        'Players/<uuid:pk>/Votes',
        PlayerVotedBy.as_view(),
        name='player_voted_by'
    ),
    path(
        'Players/<uuid:subjpk>/Vote/<uuid:objpk>',
        PlayerVoteFor.as_view(),
        name='player_vote_for'
    ),
    path(
        'AllVoted',
        AllVoted.as_view(),
        name='all_voted'
    ),
    path(
        'Votes',
        ClearVotes.as_view(),
        name='clear_votes'
    )
]