from rest_framework import serializers

from notification.models import Notification

from django.utils import timezone

from profile.models import JobApplication


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ('action', 'detail',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['created_at'] = self.get_created_at(instance)
        response['source_id'] = self.get_source_id(instance)
        response['source_name'] = f'{instance.source.first_name} {instance.source.last_name}'
        try:
            response['source_avatar'] = self.context['request'].build_absolute_uri(
                instance.source.avatar.url)
        except:
            response['source_avatar'] = None
        return response

    def get_source_id(self, instance):
        if instance.action == 'application_accepted':
            return instance.action_id
        return instance.source.id

    def get_created_at(self, instance):
        time = timezone.localtime(timezone.now()) - instance.created_at
        if time.days < 7:
            if time.days == 0:
                created_at = 'today'
            elif time.days == 1:
                created_at = 'yesterday'
            else:
                created_at = f'{time.days} days'
        elif time.days < 30:
            if int(time.days/7) == 1:
                created_at = '1 week'
            else:
                created_at = f'{int(time.days/7)} weeks'
        elif time.days < 365:
            if int(time.days/30) == 1:
                created_at = '1 month'
            else:
                created_at = f'{int(time.days/30)} months'
        else:
            if int(time.days/365) == 1:
                created_at = '1 year'
            else:
                created_at = f'{int(time.days/365)} years'
        return created_at
