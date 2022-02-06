from django.urls import path, include
from .views import *

app_name = 'Players'
urlpatterns = [
    path('Players', PlayersView.as_view()),
    path('Players/<uuid:pk>', PlayersDetail.as_view()),
    path('Players/<uuid:pk>/Vote', PlayerVote.as_view()),
    path('Players/<uuid:subjpk>/Vote/<uuid:objpk>', PlayerVoteFor.as_view())
]