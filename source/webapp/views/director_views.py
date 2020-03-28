from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

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


class DirectorCreateView(PermissionRequiredMixin, CreateView):
    model = Director
    template_name = 'director/create.html'
    form_class = DirectorForm
    permission_required = 'webapp.add_director'

    def get_success_url(self):
        return reverse('webapp:director_detail', kwargs={'pk': self.object.pk})


class DirectorUpdateView(PermissionRequiredMixin, UpdateView):
    model = Director
    template_name = 'director/update.html'
    form_class = DirectorForm
    permission_required = 'webapp.change_director'

    def get_success_url(self):
        return reverse('webapp:director_detail', kwargs={'pk': self.object.pk})


class DirectorDeleteView(PermissionRequiredMixin, DeleteView):
    model = Director
    template_name = 'director/delete.html'
    success_url = reverse_lazy('webapp:director_list')
    permission_required = 'webapp.delete_director'
