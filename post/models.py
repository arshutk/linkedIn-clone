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
    
   
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
        
# class Comment(models.Model):
#     text        = models.CharField(max_length = 50)
#     document    = models.ForeignKey(Document, on_delete = models.CASCADE, related_name = 'doc_comment')
#     commenter   = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="commented_by")

#     def __str__(self):
#             return self.text 