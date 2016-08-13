from django.conf.urls import url

from apps.views import MyRoundList
from users import views

urlpatterns = [
    url(r'^/facebook-auth$', views.facebookAuth),
    # age setting
    url(r'^$', views.UserDetail.as_view()),
    # my round
    url(r'^/rounds$', MyRoundList.as_view()),
]