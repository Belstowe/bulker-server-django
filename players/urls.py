from django.urls import path, include
from .views import *

app_name = 'Players'
urlpatterns = [
    path('Players/', PlayersView.as_view())
]