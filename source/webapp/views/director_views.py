from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView

from webapp.forms import DirectorForm
from webapp.models import Director, Movie


class DirectorListView(ListView):
    model = Director
    template_name = 'director/list.html'
    context_object_name = 'directors'
    paginate_by = 12


class DirectorDetailView(DetailView):
    model = Director
    template_name = 'director/detail.html'
    context_object_name = 'director'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['movies'] = Movie.objects.filter(directed_by__director=self.get_object())
        return context


class DirectorCreateView(CreateView):
    model = Director
    template_name = 'director/create.html'
    form_class = DirectorForm

    def get_success_url(self):
        return reverse('webapp:director_detail', kwargs={'pk': self.object.pk})
