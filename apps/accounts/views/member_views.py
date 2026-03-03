from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from apps.accounts.models import Member
from apps.accounts.forms import MemberForm

class MemberListView(ListView):
    model = Member
    context_object_name = 'members'
    template_name = 'members/list.html'
    paginate_by = 10


class MemberCreateView(CreateView):
    model = Member
    template_name = 'members/create.html'
    form_class = MemberForm
    success_url = reverse_lazy('accounts:members')