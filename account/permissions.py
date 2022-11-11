from rest_framework.permissions import BasePermission, SAFE_METHODS


class CreateOrNeedAuthenticate(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST': # just anonymous users can create account
            return not request.user.is_authenticated
        elif request.method in SAFE_METHODS: # safemethods are allowed for anonymous users
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        private_methods = ['PUT', 'PATCH', 'DELETE']
        if request.method in private_methods: # just owner accounts can delete or edit account
            return request.user == obj
        return True