from django.db import models

from userauth.models import UserProfile

class Chat(models.Model):
    time_created = models.DateTimeField(auto_now_add = True)
    text         = models.TextField(max_length = 500)
    file         = models.FileField(upload_to='chat/', null = True, blank = True, max_length = 10485760)
    sender       = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name = "sent_msgs" )
    receiver     = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name = "received_msgs")

    def __str__(self):
        return f'{self.sender.user.email} > {self.receiver.user.email}'
    
    class Meta:
        ordering = ('-time_created',)