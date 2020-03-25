from django.db.models import Count
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.base import View

from webapp.forms import RatingForm
from webapp.models import Movie, Genre


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slider_movies'] = Movie.objects.all()[:6]
        context['movies'] = Movie.objects.all()
        context['genres'] = Genre.objects.filter(movies__isnull=False).annotate(count=Count('movies')).order_by('-count')[:4]
        context['new_movies'] = Movie.objects.all().order_by('-release_date')[:5]
        return context


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie_detail.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['related_movies'] = Movie.objects.filter(genres__genre__in=self.get_object().get_genres()).distinct().\
            exclude(pk=self.get_object().pk)
        context['rating_form'] = RatingForm()
        return context


class RatingCreateView(View):

    def post(self, request, *args, **kwargs):
        movie = Movie.objects.get(pk=request.POST.get('movie'))
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.movie = movie
            rating.reviewer = request.user
            rating.save()
            return redirect('webapp:movie_detail', pk=movie.pk)
        else:
            context = {'related_movies': Movie.objects.filter(
                genres__genre__in=movie.get_genres()).distinct(). \
                exclude(pk=movie.pk), 'rating_form': form,
                       'movie': movie}
            return render(request, 'movies/movie_detail.html', context=context)


class MovieGenreView(ListView):
    model = Movie
    template_name = 'movies/genre_list.html'
    paginate_by = 6
    paginate_orphans = 0


    def get_queryset(self):
        genre = Genre.objects.get(slug=self.kwargs.get('slug'))
        return Movie.objects.filter(genres__genre=genre)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genre'] = Genre.objects.get(slug=self.kwargs.get('slug'))
        return context


