from django.shortcuts import render

from rest_framework import views, generics, viewsets

from rest_framework import status

from rest_framework.response import Response

import json

from userauth.models import UserProfile

from notification.models import Notification

from notification.serializers import NotificationSerializer

from django.http import Http404

from network.models import Connection

from django.shortcuts import get_object_or_404


class GetNotificationView(views.APIView):
    def get(self, request, profile_id):
        user = get_object_or_404(UserProfile, id = profile_id)
        query = Notification.objects.filter(target = user)
        serializer = NotificationSerializer(query, many = True, context = {'request': request})
        return Response(serializer.data, status = status.HTTP_200_OK)
