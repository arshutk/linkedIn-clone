from django.contrib import admin

from post.models import Post, Vote, Comment, Reply, Hashtag


admin.site.register(Post)
admin.site.register(Vote)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Hashtag)
