from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^/facebook-auth$', views.facebookAuth),
    # age setting
    url(r'^$', views.ageSetting),
    # my round
    url(r'^/rounds$', views.myOpenRound),
]