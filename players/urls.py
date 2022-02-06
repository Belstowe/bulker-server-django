from django.urls import path, include
from .views import *

app_name = 'Players'
urlpatterns = [
    path('Players', PlayersView.as_view()),
    path('Players/<uuid:pk>', PlayerDetail.as_view()),
    path('Players/<uuid:pk>/Vote', PlayerVotedFor.as_view()),
    path('Players/<uuid:pk>/Votes', PlayerVotedBy.as_view()),
    path('Players/<uuid:subjpk>/Vote/<uuid:objpk>', PlayerVoteFor.as_view()),
    path('AllVoted', AllVoted.as_view()),
    path('Votes', ClearVotes.as_view())
]