from rest_framework.permissions import BasePermission, SAFE_METHODS


class CreateOrNeedAuthenticate(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return request.user.is_staff or request.user == obj
        elif request.method == 'PUT' or request.method == 'PATCH':
            return request.user == obj
        return True
        