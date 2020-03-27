from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from webapp.forms import GenreForm
from webapp.models import Genre


class GenreCreateView(CreateView):
    template_name = 'genre/create.html'
    model = Genre
    form_class = GenreForm
    success_url = reverse_lazy('webapp:genre_list')


class GenreListView(ListView):
    template_name = 'genre/list.html'
    model = Genre
    context_object_name = 'genres'

