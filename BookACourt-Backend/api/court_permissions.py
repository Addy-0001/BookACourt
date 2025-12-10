from rest_framework import permissions


class IsCourtOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission for court owners
    Allows read access to all, write access only to court owners
    """

    def has_permission(self, request, view):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for the court owner or super user
        return (
            request.user and
            request.user.is_authenticated and
            (obj.owner == request.user or request.user.is_super_user)
        )


class IsCourtOwnerOrManager(permissions.BasePermission):
    """
    Permission for court owner or managers
    """

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        # Super users have full access
        if request.user.is_super_user:
            return True

        # Check if user is the owner
        if hasattr(obj, 'owner') and obj.owner == request.user:
            return True

        # Check if user is a manager
        if hasattr(obj, 'managers') and obj.managers.filter(id=request.user.id).exists():
            return True

        # For objects related to a court (like reviews, pricing)
        if hasattr(obj, 'court'):
            court = obj.court
            return request.user.can_manage_court(court)

        return False


class IsPlayerOrReadOnly(permissions.BasePermission):
    """
    Permission for players to create reviews
    Others can only read
    """

    def has_permission(self, request, view):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for players
        return (
            request.user and
            request.user.is_authenticated and
            request.user.is_player
        )

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for the player who created the review
        return (
            request.user and
            request.user.is_authenticated and
            obj.player == request.user
        )


class IsSuperUserOrReadOnly(permissions.BasePermission):
    """
    Permission for super users only
    Others can only read
    """

    def has_permission(self, request, view):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for super users
        return (
            request.user and
            request.user.is_authenticated and
            request.user.is_super_user
        )
