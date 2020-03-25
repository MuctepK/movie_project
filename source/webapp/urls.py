from django.urls import path

from webapp.views import IndexView, MovieDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),

]

app_name = 'webapp'
