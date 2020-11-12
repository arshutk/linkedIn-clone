from django.contrib import admin

from post.models import Post, Vote

admin.site.register(Post)
admin.site.register(Vote)
