from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import RegistrationView, ProfileDetailView, ProfileUpdateView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('user/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('user/<int:pk>/update/', ProfileUpdateView.as_view(), name='profile_update')

]

app_name = 'accounts'
