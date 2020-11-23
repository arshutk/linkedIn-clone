from django.db import models

from userauth.models import UserProfile

class Network(models.Model):
    user       = models.OneToOneField(UserProfile, on_delete = models.CASCADE, related_name = 'network')
    connection = models.ManyToManyField(UserProfile, through = 'Connection', through_fields = ('network', 'sender'), related_name = 'connections')
    followers  = models.ManyToManyField(UserProfile, related_name ='followers', blank = True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
class Connection(models.Model):
    network                = models.ForeignKey(Network, on_delete = models.CASCADE, related_name = 'network')
    receiver               = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name = 'request_received')
    sender                 = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name = 'request_sent')
    date_time              = models.DateTimeField(auto_now = True)
    has_been_accepted      = models.BooleanField(default = False)
    is_visible             = models.BooleanField(default = True)
    
    def __str__(self):
        return f'{self.sender.first_name} {self.sender.last_name} > {self.receiver.first_name} {self.receiver.last_name}'



