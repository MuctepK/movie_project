from django import forms
from django.forms import formset_factory, inlineformset_factory

from webapp.models import Rating, Movie, Genre, Actor, Director


class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        exclude = []


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['title']


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'text']


class MovieForm(forms.ModelForm):
    photo = forms.ImageField(required=False, label='Постер')

    class Meta:
        model = Movie
        exclude = []


class GenreFormsetForm(forms.Form):
    title = forms.ModelChoiceField(queryset=Genre.objects.all(), label='Жанр')


class ActorFormsetForm(forms.Form):
    actor = forms.ModelChoiceField(queryset=Actor.objects.all(), label = 'Актёр')


class DirectorFormSetForm(forms.Form):
    director = forms.ModelChoiceField(queryset=Director.objects.all(), label = 'Режиссёр')


GenreFormSet = formset_factory(GenreFormsetForm, extra=0, min_num=1, max_num=10, can_delete=True)
ActorFormSet = formset_factory(ActorFormsetForm, extra=0, min_num=1, max_num=10, can_delete=True)
DirectorFormSet = formset_factory(DirectorFormSetForm, extra=0, min_num=1, max_num=10, can_delete=True)


