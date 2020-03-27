from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from webapp.forms import ActorForm
from webapp.models import Actor, Movie


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


class ActorDetailView(DetailView):
    template_name = 'actor/detail.html'
    model = Actor

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['movies'] = Movie.objects.filter(acted_by__actor=self.get_object())
        return context
