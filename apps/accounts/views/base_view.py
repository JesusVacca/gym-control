from django.shortcuts import get_object_or_404, redirect
from django.views import View
from utils import Notify


class BaseDeleteViewMixin(View):
    model = None
    redirect_url = None
    def post(self, request, pk):
        search = get_object_or_404(self.model, pk=pk)
        level = None
        try:
            search.delete()
            message = 'Usuario eliminado correctamente'
        except Exception as e:
            message = 'No fue posible eliminar el usuario'
            level = 'error'

        Notify.notify(
            request=request,
            message=message,
            level=level,
        )
        return redirect(self.redirect_url)

class BaseToggleViewMixin(View):
    model = None
    redirect_url = None
    def post(self, request, pk):
        search = get_object_or_404(self.model, pk=pk)
        search.is_active = not search.is_active
        search.save()
        return redirect(self.redirect_url)