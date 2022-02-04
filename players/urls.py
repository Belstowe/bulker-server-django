from django.urls import path, include
from .views import *

app_name = 'Players'
urlpatterns = [
    path('/', PlayersView.as_view())
]