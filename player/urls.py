from django.conf.urls import url

from rest_framework.authtoken import views

import player.views as player_views


urlpatterns = [
    url(r'^api/users/register$', player_views.UserRegistrationView.as_view()),
    url(r'^api/users/activate$', player_views.UserActivationView.as_view()),
    url(r'^api/password/forgot$', player_views.PasswordResetView.as_view()),
    url(r'^api/password/change$', player_views.ChangePasswordView.as_view()),
    url(r'^api/users/login$', views.obtain_auth_token),
    url(r'^api/users/me$', player_views.UserDetailsView.as_view()),
]
