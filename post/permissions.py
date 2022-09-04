from rest_framework.permissions import BasePermission, SAFE_METHODS


# ============================= PERMISSION FOR COMMENTS =========================
class IsOwnerOrAuthorPost(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return obj.post.author == request.user or obj.owner == request.user
        elif request.method == 'PUT' or request.method == 'PATCH':
            return request.user == obj.owner
        return True


# ============================= PERMISSION FOR POSTS ============================
class IsAuthorOrReadonly(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.author