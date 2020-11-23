from django.contrib import admin

from network.models import Network, Connection

class ConnectionInline(admin.TabularInline):
    model = Connection

class NetworkAdmin(admin.ModelAdmin):
    inlines = [
        ConnectionInline,
    ]
    
admin.site.register(Network, NetworkAdmin)
