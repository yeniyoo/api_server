from django.conf.urls import url

from apps.views import MyRoundList
from users import views

urlpatterns = [
    url(r'^/facebook-auth$', views.facebookAuth),
    # User related
    url(r'^$', views.users),
    # my round
    url(r'^/rounds$', MyRoundList.as_view()),
]