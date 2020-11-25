from django.db import models

from userauth.models import UserProfile

class Connection(models.Model):
    
    receiver               = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name = 'request_received')
    sender                 = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name = 'request_sent')
    date_time              = models.DateTimeField(auto_now = True)
    has_been_accepted      = models.BooleanField(default = False)
    is_visible             = models.BooleanField(default = True)
    
    def __str__(self):
        return f'{self.sender.first_name} {self.sender.last_name} > {self.receiver.first_name} {self.receiver.last_name}'