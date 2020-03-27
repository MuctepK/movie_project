from django.urls import path

from webapp.views import IndexView, MovieDetailView, RatingCreateView, MovieGenreView, MovieCreateView, MovieUpdateView, \
    MovieDeleteView, GenreCreateView, GenreListView, GenreUpdateView, GenreDeleteView, ActorListView, ActorCreateView, \
    ActorDetailView, ActorUpdateView, ActorDeleteView, DirectorListView, DirectorDetailView, DirectorCreateView, \
    DirectorUpdateView, DirectorDeleteView, RatingUpdateView, RatingDeleteView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('movies/create/', MovieCreateView.as_view(), name='movie_create'),
    path('movies/<int:pk>/update/', MovieUpdateView.as_view(), name='movie_update'),
    path('movies/<int:pk>/delete/', MovieDeleteView.as_view(), name='movie_delete'),
    path('movies/<str:slug>', MovieGenreView.as_view(), name='movie_genre'),
    path('genres/create/', GenreCreateView.as_view(), name='genre_create'),
    path('genres/', GenreListView.as_view(), name='genre_list'),
    path('genres/<int:pk>/update/', GenreUpdateView.as_view(), name='genre_update'),
    path('genres/<int:pk>/delete/', GenreDeleteView.as_view(), name='genre_delete'),
    path('actors/list/', ActorListView.as_view(), name='actor_list'),
    path('actors/create/', ActorCreateView.as_view(), name='actor_create'),
    path('actors/<int:pk>/', ActorDetailView.as_view(), name='actor_detail'),
    path('actors/<int:pk>/update/', ActorUpdateView.as_view(), name='actor_update'),
    path('actors/<int:pk>/delete/', ActorDeleteView.as_view(), name='actor_delete'),
    path('directors/', DirectorListView.as_view(), name='director_list'),
    path('directors/create/', DirectorCreateView.as_view(), name='director_create'),
    path('directors/<int:pk>/', DirectorDetailView.as_view(), name='director_detail'),
    path('directors/<int:pk>/update/', DirectorUpdateView.as_view(), name='director_update'),
    path('directors/<int:pk>/delete/', DirectorDeleteView.as_view(), name='director_delete'),
    path('rating/create/', RatingCreateView.as_view(), name='rating_create'),
    path('rating/<int:pk>/update/', RatingUpdateView.as_view(), name='rating_update'),
    path('rating/<int:pk>/delete/', RatingDeleteView.as_view(), name='rating_delete'),
]

app_name = 'webapp'
