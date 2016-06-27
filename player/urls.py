from django.conf.urls import url

from simple_login import views as simple_login_views

import player.views as player_views
from player.models import User


urlpatterns = [
    url(
        r'^api/users/register$',
        player_views.UserRegistrationView.as_view()
    ),
    url(
        r'^api/users/request_activation_key$',
        simple_login_views.RequestActivationKey.as_view(user_model=User)
    ),
    url(
        r'^api/users/activate$',
        player_views.ActivateAccount.as_view(user_model=User)
    ),
    url(
        r'^api/password/forgot$',
        simple_login_views.RequestPasswordReset.as_view(
            user_model=User
        )
    ),
    url(
        r'^api/password/change$',
        simple_login_views.ChangePassword.as_view(user_model=User)
    ),
    url(
        r'^api/users/login$',
        player_views.Login.as_view(user_model=User)
    ),
    url(
        r'^api/users/me$',
        player_views.RetrieveUpdateDestroyProfile.as_view()
    ),
    url(
        r'^api/users/status$',
        simple_login_views.AccountStatus.as_view(user_model=User)
    ),
]
