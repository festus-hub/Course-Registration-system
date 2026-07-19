from rest_framework import permissions


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Anyone authenticated can read (GET/HEAD/OPTIONS).
    Only staff can write (POST/PUT/PATCH/DELETE).
    Used for Department and Course — students need to browse these,
    but only admins should be able to create/edit/delete them.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsStaffOnly(permissions.BasePermission):
    """
    Only staff can access at all, read or write.
    Used for Student — a full list of every student's record
    is sensitive and shouldn't be browsable by other students.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff