from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsProfessor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "professor"

class IsOwnerOrReadOnly(BasePermission):
    """
    Permite que apenas o dono do objeto edite ou delete.
    """
    def has_object_permission(self, request, view, obj):
        # Permissões de leitura são permitidas para qualquer request
        if request.method in SAFE_METHODS:
            return True

        # Permissões de escrita são permitidas apenas para o dono do objeto
        return obj.autor == request.user