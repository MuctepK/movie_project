from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

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

    def get_success_url(self):
        return reverse('webapp:actor_detail', kwargs={'pk': self.object.pk})


class ActorDetailView(DetailView):
    template_name = 'actor/detail.html'
    model = Actor

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['movies'] = Movie.objects.filter(acted_by__actor=self.get_object())
        return context


class ActorUpdateView(UpdateView):
    template_name = 'actor/update.html'
    model = Actor
    form_class = ActorForm

    def get_success_url(self):
        return reverse('webapp:actor_detail', kwargs={'pk': self.get_object().pk})


class ActorDeleteView(DeleteView):
    template_name = 'actor/delete.html'
    model = Actor
    success_url = reverse_lazy('webapp:actor_list')
