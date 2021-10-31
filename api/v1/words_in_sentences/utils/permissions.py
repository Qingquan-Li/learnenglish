from rest_framework import permissions


# www.django-rest-framework.org/tutorial/4-authentication-and-permissions/#object-level-permissions
class IsSentenceCreatorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow creator of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to
        # the creator(field: created_by) of the sentence.
        return obj.created_by == request.user


# # :( invalid
# class IsAdminUserOrReadOnly(permissions.BasePermission):
#     """
#     Custom permission to only allow admin user to edit it.
#     """
#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return request.user and request.user.is_staff
