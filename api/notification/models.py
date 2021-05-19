from django.db import models

from userauth.models import UserProfile

class Notification(models.Model):
    TYPE = (
                ('post_liked','post_liked'), #
                ('comment_liked','comment_liked'), #
                ('reply_liked','reply_liked'), #
                ('commented','commented'), #
                ('viewed','viewed'),
                ('replied','replied'), #
                ('application_accepted','application_accepted'), #
               )
    action = models.CharField(choices = TYPE, max_length = 20)
    target  = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name = 'notifications')
    source  = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name = 'notifications_made')
    created_at = models.DateTimeField(auto_now_add = True)
    detail  = models.TextField() 
    action_id = models.IntegerField()
    
    
