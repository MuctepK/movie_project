from django.contrib.auth.forms import AuthenticationForm


def forms(request):
    auth_form = AuthenticationForm() if not request.user.is_authenticated else None
    return {
        'auth_form': auth_form
    }
