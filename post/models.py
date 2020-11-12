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
   video_linked      = models.FileField(upload_to='article/videos/', blank = True, null = True, max_length = 5242880)
   doc_linked        = models.FileField(upload_to='article/docs', blank = True, null = True, max_length = 2621440)
   
   written_by        = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="writiten_by")  
   bookmarked_by     = models.ManyToManyField(UserProfile, related_name="bookmarked_by", blank = True)
   
   def __str__(self):
      return f'{self.written_by.first_name} {self.written_by.last_name} > {self.text}[:30]'
    
      
   
class Vote(models.Model):
   like              = models.IntegerField(default = 0)
   celebrate         = models.IntegerField(default = 0)
   support           = models.IntegerField(default = 0)
   love              = models.IntegerField(default = 0)
   insightful        = models.IntegerField(default = 0)
   curious           = models.IntegerField(default = 0)
   post              = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="votes")
   upvoter           = models.ManyToManyField(UserProfile, related_name = "upvoter", blank = True)
   downvoter         = models.ManyToManyField(UserProfile, related_name = "downvoter", blank = True)
   
        
   def __str__(self):
      return f'{self.post.written_by.first_name} {self.post.written_by.last_name} > {self.post.text}[:30]'
    
   class Meta:
      ordering = ('-like', '-celebrate', '-support', '-love', '-insightful', '-curious',)
        
        
# class Comment(models.Model):
#     text        = models.CharField(max_length = 50)
#     document    = models.ForeignKey(Document, on_delete = models.CASCADE, related_name = 'doc_comment')
#     commenter   = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="commented_by")

#     def __str__(self):
#             return self.text 