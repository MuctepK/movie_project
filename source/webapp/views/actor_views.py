from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from webapp.forms import ActorForm
from webapp.models import Actor


class ActorListView(ListView):
    template_name = 'actor/list.html'
    model = Actor
    context_object_name = 'actors'
    paginate_by = 12


class ActorCreateView(CreateView):
    template_name = 'actor/create.html'
    model = Actor
    form_class = ActorForm
    success_url = reverse_lazy('webapp:actor_list')
