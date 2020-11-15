from django.contrib import admin

from post.models import Post, Vote, Comment, Reply


admin.site.register(Post)
admin.site.register(Vote)
admin.site.register(Comment)
admin.site.register(Reply)
