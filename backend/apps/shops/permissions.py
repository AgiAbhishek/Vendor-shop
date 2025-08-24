from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    message = 'You do not have permission to access this shop.'

    def has_object_permission(self, request, view, obj):
        return getattr(obj, 'vendor_id', None) == request.user.id