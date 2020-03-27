from django.urls import path

from webapp.views import IndexView, MovieDetailView, RatingCreateView, MovieGenreView, MovieCreateView, MovieUpdateView, \
    MovieDeleteView, GenreCreateView, GenreListView, GenreUpdateView, GenreDeleteView, ActorListView, ActorCreateView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('movies/create/', MovieCreateView.as_view(), name='movie_create'),
    path('movies/<int:pk>/update/', MovieUpdateView.as_view(), name='movie_update'),
    path('movies/<int:pk>/delete/', MovieDeleteView.as_view(), name='movie_delete'),
    path('rating/create/', RatingCreateView.as_view(), name='rating_create'),
    path('movies/<str:slug>', MovieGenreView.as_view(), name='movie_genre'),
    path('genres/create/', GenreCreateView.as_view(), name='genre_create'),
    path('genres/', GenreListView.as_view(), name='genre_list'),
    path('genres/<int:pk>/update/', GenreUpdateView.as_view(), name='genre_update'),
    path('genres/<int:pk>/delete/', GenreDeleteView.as_view(), name='genre_delete'),
    path('actors/list/', ActorListView.as_view(), name='actor_list'),
    path('actors/create/', ActorCreateView.as_view(), name='actor_create'),
]

app_name = 'webapp'
