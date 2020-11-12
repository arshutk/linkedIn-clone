from django.db import models

from userauth.models import UserProfile

# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160

class Post(models.Model):
   text              = models.TextField() 
   image_linked      = models.ImageField(upload_to = 'article/images/', blank = True, null = True, max_length = 1048576) 
   video_linked      = models.FileField(upload_to = 'article/videos/', blank = True, null = True, max_length = 5242880)
   doc_linked        = models.FileField(upload_to = 'article/docs', blank = True, null = True, max_length = 2621440)
   
   written_by        = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="articles")  
   bookmarked_by     = models.ManyToManyField(UserProfile, related_name="bookmarked_posts", blank = True)
   posted_at         = models.DateTimeField(auto_now_add = True)
   
   def __str__(self):
      return f'{self.written_by.first_name} {self.written_by.last_name} : {self.text[:30]}'
    
      
   
class Vote(models.Model):
   vote              = models.IntegerField(default = 0)
   post              = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="votes")
   upvoter           = models.ManyToManyField(UserProfile, through = "Upvoter", blank = True, related_name = 'up_voter')
   downvoter         = models.ManyToManyField(UserProfile, through = "Downvoter", blank = True, related_name = 'down_voter')
   
        
   def __str__(self):
      return f'{self.post.written_by.first_name} {self.post.written_by.last_name} : {self.post.text[:30]} : {self.vote}'
    
   class Meta:
      ordering = ('-vote',)
 
   
class Upvoter(models.Model):
   VOTE_TYPE  = (
                ('like','like'),
                ('celebrate','celebrate'),
                ('support','support'),
                ('love','love'),
                ('insightful','insightful'),
                ('curious','curious'),
               )
   
   vote                 = models.ForeignKey(Vote, on_delete = models.CASCADE, related_name = 'up_vote')
   user                 = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
   vote_type            = models.CharField(max_length = 35, choices = VOTE_TYPE, default = 'like')
   

class Downvoter(models.Model):
   VOTE_TYPE  = (
                ('like','like'),
                ('celebrate','celebrate'),
                ('support','support'),
                ('love','love'),
                ('insightful','insightful'),
                ('curious','curious'),
               )
   
   vote                 = models.ForeignKey(Vote, on_delete = models.CASCADE, related_name = 'down_vote')
   user                 = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
   vote_type            = models.CharField(max_length = 35, choices = VOTE_TYPE, default = 'like')
   
        
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
        
# class Comment(models.Model):
#     text        = models.CharField(max_length = 50)
#     document    = models.ForeignKey(Document, on_delete = models.CASCADE, related_name = 'doc_comment')
#     commenter   = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="commented_by")

#     def __str__(self):
#             return self.text 