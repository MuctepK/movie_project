from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView

from accounts.forms import RegistrationForm, UserForm, ProfileForm


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


class ProfileUpdateView(UpdateView):
    template_name = 'profile_update.html'
    model = User
    form_class = UserForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profile_form'] = ProfileForm(instance=self.object.profile)
        return context

    def post(self, request, *args, **kwargs):
        user_form, profile_form = UserForm(request.POST, instance=self.get_object()), ProfileForm(request.POST, request.FILES, instance=self.get_object().profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('accounts:profile_detail', pk= user_form.instance.pk)
        return render(request, self.template_name, context={'form': user_form, 'profile_form': profile_form})
