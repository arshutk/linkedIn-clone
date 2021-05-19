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
   
   # Remove later
   media_type        = models.CharField(max_length = 6, null = True)
   
   written_by        = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="articles")  
   bookmarked_by     = models.ManyToManyField(UserProfile, related_name="bookmarked_posts", blank = True)
   posted_at         = models.DateTimeField(auto_now_add = True)
      
   def __str__(self):
      return f'{self.written_by.first_name} {self.written_by.last_name} : {self.text[:30]}'
    
   class Meta:
      ordering = ('-posted_at',)
   
   
class Vote(models.Model):
   CHOICE = (  
             ('like','like'),
             ('celebrate','celebrate'),
             ('support','support'),
             ('love','love'),
             ('insightful','insightful'),
             ('curious','curious')
            )
   
   post              = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = "votes")
   vote_type         = models.CharField(choices = CHOICE, default = None, max_length = 10)
   voter             = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name = "votes")
    
   
class Comment(models.Model):
   post         = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "comments")
   commented_by = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name = "comments_made")
   text         = models.TextField()
   posted_at    = models.DateTimeField(auto_now_add = True)
   
   liked_by     = models.ManyToManyField(UserProfile, blank = True, related_name = "comments_liked")
   
   def __str__(self):
      return f'{self.commented_by.first_name} {self.commented_by.last_name} >  : {self.post.text[:30]}'
    
   class Meta:
      ordering = ('-posted_at',)
  
      
class Reply(models.Model):
   comment     = models.ForeignKey(Comment, on_delete = models.CASCADE, related_name = "replies")
   replied_by  = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name = "replies_made")
   text        = models.TextField()
   posted_at   = models.DateTimeField(auto_now_add = True)
   
   liked_by    = models.ManyToManyField(UserProfile, blank = True, related_name = "replies_liked")
   
   def __str__(self):
      return f'{self.replied_by.first_name} {self.replied_by.last_name} : {self.comment.text[:30]}'
    
   class Meta:
      ordering = ('-posted_at',)
      

class Hashtag(models.Model):
   topic       = models.CharField(max_length = 50)
   time        = models.DateTimeField(auto_now_add = True)
   
   def __str__(self):
      return f'{self.topic} {self.time.date()}'
   