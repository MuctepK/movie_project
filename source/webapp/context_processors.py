from django.contrib.auth.forms import AuthenticationForm

from webapp.models import Genre


def forms(request):
    auth_form = AuthenticationForm() if not request.user.is_authenticated else None
    genres = Genre.objects.filter(movies__isnull=False).distinct()
    print(genres)
    return {
        'auth_form': auth_form,
        'menu_genres': genres,
    }
