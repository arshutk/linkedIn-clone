from django.contrib import admin

from post.models import Post, Vote, Upvoter, Downvoter

admin.site.register(Post)
admin.site.register(Vote)
admin.site.register(Upvoter)
admin.site.register(Downvoter)
