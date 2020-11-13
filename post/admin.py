from django.contrib import admin

from post.models import Post, Vote
# , Like, Celebrate, Support, Love, Insightful, Curious, Vot


admin.site.register(Post)
# admin.site.register(Like)
# admin.site.register(Celebrate)
# admin.site.register(Support)
# admin.site.register(Love)
# admin.site.register(Insightful)
# admin.site.register(Curious)
admin.site.register(Vote)
