from rest_framework.permissions import BasePermission, SAFE_METHODS


class QuizPermission(BasePermission):
    """
    Permissions for Quiz endpoints.

    Rules:
    - User must be authenticated for all actions.
    - Create & List: any authenticated user.
    - Retrieve / Update / Delete: only the owner of the quiz.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user