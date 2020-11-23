from django.contrib import admin

from chat.models import Thread, Chat

class ChatInline(admin.TabularInline):
    model = Chat

class ThreadAdmin(admin.ModelAdmin):
    inlines = [
        ChatInline,
    ]
    
admin.site.register(Thread, ThreadAdmin)
