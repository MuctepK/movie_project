from django.urls import path

from webapp.views import IndexView, MovieDetailView, RatingCreateView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('rating/create/', RatingCreateView.as_view(), name='rating_create'),
]

app_name = 'webapp'
