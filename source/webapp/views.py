from django.shortcuts import render
from django.views.generic import TemplateView

from webapp.models import Movie


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slider_movies'] = Movie.objects.all()[:7]
        return context
