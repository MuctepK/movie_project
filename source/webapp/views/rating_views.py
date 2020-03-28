from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import UpdateView, DeleteView
from django.views.generic.base import View

from webapp.forms import RatingForm
from webapp.models import Movie, Rating


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


class RatingUpdateView(UserPassesTestMixin, UpdateView):
    model = Rating
    template_name = 'rating/update.html'
    form_class = RatingForm

    def get_success_url(self):
        return reverse('webapp:movie_detail', kwargs={'pk': self.object.movie.pk})

    def test_func(self):
        return self.request.user == self.object.reviewer


class RatingDeleteView(UserPassesTestMixin, DeleteView):
    model = Rating
    template_name = 'rating/delete.html'

    def post(self, request, *args, **kwargs):
        self.movie = self.get_object().movie
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:movie_detail', kwargs={'pk': self.movie.pk})

    def test_func(self):
        return self.request.user == self.object.reviewer
