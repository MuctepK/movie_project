from django.db.models import Count
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from webapp.models import Movie, Genre


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slider_movies'] = Movie.objects.all()[:6]
        context['movies'] = Movie.objects.all()
        context['genres'] = Genre.objects.filter(movies__isnull=False).annotate(count=Count('movies')).order_by('-count')[:4]
        context['new_movies'] = Movie.objects.all().order_by('-release_date')[:5]
        print(context['genres'])
        return context


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie_detail.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['related_movies'] = Movie.objects.filter(genres__genre__in=self.get_object().get_genres()).distinct().\
            exclude(pk=self.get_object().pk)
        return context

