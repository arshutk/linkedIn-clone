from django.shortcuts import render

from rest_framework import viewsets

from django.shortcuts import render

from rest_framework import status

from rest_framework.response import Response

from chat.models import Chat

from userauth.models import UserProfile

from userauth.serializers import UserProfileSerializer

from django.http import Http404

from network.models import Connection

from django.shortcuts import get_object_or_404

from chat.serializers import ChatSerializer

from rest_framework import views

