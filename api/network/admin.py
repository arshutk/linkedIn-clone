from django.contrib import admin

from network.models import Connection, Follow

# class ConnectionInline(admin.TabularInline):
#     model = Connection

# class NetworkAdmin(admin.ModelAdmin):
#     inlines = [
#         ConnectionInline,
#     ]
    
admin.site.register(Connection)
admin.site.register(Follow)
