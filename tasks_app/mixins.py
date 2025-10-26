from django.core.exceptions import PermissionDenied

class UserIsOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.creator != request.user:
            raise PermissionDenied("You don't have permission to edit this task.")
        return super().dispatch(request, *args, **kwargs)