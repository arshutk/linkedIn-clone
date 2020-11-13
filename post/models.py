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
    
       
        
class Like(models.Model):
   
   post              = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="likes")
   vote              = models.IntegerField(default = 0)
   upvoter           = models.ManyToManyField(UserProfile, blank = True, related_name = 'like_upvoter')
   downvoter         = models.ManyToManyField(UserProfile, blank = True, related_name = 'like_downvoter')

   def __str__(self):
      return f'{self.post.text[:30]} : like : {self.vote}'
    
   
class Celebrate(models.Model):
   
   post              = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="celebrated")
   vote              = models.IntegerField(default = 0)
   upvoter           = models.ManyToManyField(UserProfile, blank = True, related_name = 'celebrate_upvoter')
   downvoter         = models.ManyToManyField(UserProfile, blank = True, related_name = 'celebrate_downvoter')

   def __str__(self):
      return f'{self.post.text[:30]} : celebrate : {self.vote}'
    
   
class Support(models.Model):
   
   post              = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="supports")
   vote              = models.IntegerField(default = 0)
   upvoter           = models.ManyToManyField(UserProfile, blank = True, related_name = 'support_upvoter')
   downvoter         = models.ManyToManyField(UserProfile, blank = True, related_name = 'support_downvoter')

   def __str__(self):
      return f'{self.post.text[:30]} : support : {self.vote}'
    
   
class Love(models.Model):
   
   post              = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="loves")
   vote              = models.IntegerField(default = 0)
   upvoter           = models.ManyToManyField(UserProfile, blank = True, related_name = 'love_upvoter')
   downvoter         = models.ManyToManyField(UserProfile, blank = True, related_name = 'love_downvoter')

   def __str__(self):
      return f'{self.post.text[:30]} : love : {self.vote}'
    
   
class Insightful(models.Model):
   
   post              = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="insightful")
   vote              = models.IntegerField(default = 0)
   upvoter           = models.ManyToManyField(UserProfile, blank = True, related_name = 'insightful_upvoter')
   downvoter         = models.ManyToManyField(UserProfile, blank = True, related_name = 'insightful_downvoter')

   def __str__(self):
      return f'{self.post.text[:30]} : insightful {self.vote}'
    
   
class Curious(models.Model):
   
   post              = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="curious")
   vote              = models.IntegerField(default = 0)
   upvoter           = models.ManyToManyField(UserProfile, blank = True, related_name = 'curious_upvoter')
   downvoter         = models.ManyToManyField(UserProfile, blank = True, related_name = 'curious_downvoter')

   def __str__(self):
      return f'{self.post.text[:30]} : curious {self.vote}'
    
   
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
        
# class Comment(models.Model):
#     text        = models.CharField(max_length = 50)
#     document    = models.ForeignKey(Document, on_delete = models.CASCADE, related_name = 'doc_comment')
#     commenter   = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="commented_by")

#     def __str__(self):
#             return self.text 