from django.urls import path

from webapp.views import IndexView, MovieDetailView, RatingCreateView, MovieGenreView, MovieCreateView, MovieUpdateView, \
    MovieDeleteView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('movies/create/', MovieCreateView.as_view(), name='movie_create'),
    path('movies/<int:pk>/update/', MovieUpdateView.as_view(), name='movie_update'),
    path('movies/<int:pk>/delete/', MovieDeleteView.as_view(), name='movie_delete'),
    path('rating/create/', RatingCreateView.as_view(), name='rating_create'),
    path('movies/<str:slug>', MovieGenreView.as_view(), name='movie_genre')
]

app_name = 'webapp'
