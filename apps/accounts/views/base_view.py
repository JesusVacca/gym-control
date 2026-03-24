from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View, ListView
from utils import Notify


class BaseSearchView(ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search','')
        return context

    def get_queryset(self):
        queryset = self.model.objects.all().order_by('-created_at')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__contains=search) |
                Q(phone_number__contains=search) |
                Q(email__contains=search)
            )
        return queryset


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