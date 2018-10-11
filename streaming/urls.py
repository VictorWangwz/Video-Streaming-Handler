from django.contrib import admin
from django.urls import path, include
from .views import *
urlpatterns = [
    path('on_publish', on_publish),
    path('on_play', on_play),
    path('on_publish_done', on_publish_done),
    path('stream/', livefe)
]
