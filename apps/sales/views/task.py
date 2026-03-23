from django.views.generic import ListView
from apps.sales.models import SaleTask


class SaleTaskListView(ListView):
    model = SaleTask
    context_object_name = 'tasks'
    template_name = 'tasks/list.html'