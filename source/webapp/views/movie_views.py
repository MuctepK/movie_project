from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView
from django.views.generic.base import View

from webapp.forms import RatingForm, MovieForm, GenreFormSet, ActorFormSet, DirectorFormSet
from webapp.models import Movie, Genre, MovieGenre, MovieCast, MovieDirection


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


class MovieCreateView(CreateView):
    model = Movie
    template_name = 'movies/create.html'
    form_class = MovieForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['genre_formset'] = GenreFormSet(prefix='genre_formset')
        context['actor_formset'] = ActorFormSet(prefix='actor_formset')
        context['director_formset'] = DirectorFormSet(prefix='director_formset')
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        genre_formset = GenreFormSet(request.POST, prefix='genre_formset')
        actor_formset = ActorFormSet(request.POST, prefix='actor_formset')
        director_formset = DirectorFormSet(request.POST, prefix='director_formset')
        if form.is_valid() and genre_formset.is_valid() and actor_formset.is_valid() and director_formset.is_valid():
            movie = form.save()
            for genre in genre_formset:
                MovieGenre.objects.create(genre=genre.cleaned_data['title'], movie=movie)
            for actor in actor_formset:
                MovieCast.objects.create(actor=actor.cleaned_data['actor'], movie=movie)
            for director in director_formset:
                MovieDirection.objects.create(director=director.cleaned_data['director'], movie=movie)
            return redirect('webapp:movie_detail', pk=movie.pk)
        else:
            context = {'form': form, 'genre_formset': genre_formset, 'actor_formset':actor_formset, 'director_formset': director_formset}
            return render(request, self.template_name, context=context)


class MovieUpdateView(UpdateView):
    model = Movie
    template_name = 'movies/update.html'
    form_class = MovieForm
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['genre_formset'] = GenreFormSet(prefix='genre_formset',
                                                initial=[{'title': genre } for genre in self.object.get_genres()])
        context['actor_formset'] = ActorFormSet(prefix='actor_formset',
                                                initial=[{"actor": actor } for actor in self.object.get_actors()])
        context['director_formset'] = DirectorFormSet(prefix='director_formset',
                                                      initial=[{"director": director} for director in self.get_object().get_directors()])
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=self.get_object())
        genre_formset = GenreFormSet(request.POST, prefix='genre_formset')
        actor_formset = ActorFormSet(request.POST, prefix='actor_formset')
        director_formset = DirectorFormSet(request.POST, prefix='director_formset')
        if form.is_valid() and genre_formset.is_valid() and actor_formset.is_valid() and director_formset.is_valid():
            movie = form.save()
            movie.genres.all().delete()
            movie.acted_by.all().delete()
            movie.directed_by.all().delete()
            for genre in genre_formset:
                MovieGenre.objects.create(genre=genre.cleaned_data['title'], movie=movie)
            for actor in actor_formset:
                MovieCast.objects.create(actor=actor.cleaned_data['actor'], movie=movie)
            for director in director_formset:
                MovieDirection.objects.create(director=director.cleaned_data['director'], movie=movie)
            return redirect('webapp:movie_detail', pk=movie.pk)
        else:
            context = {'form': form, 'genre_formset': genre_formset, 'actor_formset':actor_formset,
                       'director_formset': director_formset, 'movie': self.get_object()}
            return render(request, self.template_name, context=context)


class MovieDeleteView(DeleteView):
    model = Movie
    template_name = 'movies/delete.html'

    def get_success_url(self):
        return reverse('webapp:index')
