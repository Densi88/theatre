from rest_framework import permissions

class Admin_permission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.userprofile.role == 'admin'
    
class Read_only_permission(permissions.BasePermission):
     def has_permission(self, request, view):
        if(request.method in permissions.SAFE_METHODS):
             return True
        return request.user.is_authenticated and request.user.userprofile.role == 'admin'
     



