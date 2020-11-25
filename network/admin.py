from django.contrib import admin

from network.models import Connection

# class ConnectionInline(admin.TabularInline):
#     model = Connection

# class NetworkAdmin(admin.ModelAdmin):
#     inlines = [
#         ConnectionInline,
#     ]
    
admin.site.register(Connection)
