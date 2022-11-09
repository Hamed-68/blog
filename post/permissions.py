from rest_framework.permissions import BasePermission, SAFE_METHODS



class IsOwnerOrAuthorPost(BasePermission):
    """ PERMISSION FOR COMMENTS """
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return obj.post.author == request.user or obj.owner == request.user
        return True



class IsAuthorOrReadonly(BasePermission):
    """ PERMISSION FOR POSTS """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.author



class IsLikerOrReadonly(BasePermission):
    """ PERMISSION FOR POST LIKE """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.user