from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import CreateView, DetailView

from accounts.forms import RegistrationForm


class RegistrationView(CreateView):
    template_name = 'registration/registration.html'
    form_class = RegistrationForm
    model = None

    def get_success_url(self):
        return reverse('webapp:index')


class ProfileDetailView(DetailView):
    template_name = 'profile.html'
    model = User
    context_object_name = 'user'