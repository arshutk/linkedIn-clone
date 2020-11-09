from rest_framework import permissions


class IsAuthenticatedAndOwner(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.user 
        # return request.user and request.user.admin
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user.profile 