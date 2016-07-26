from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^/facebook-auth', views.facebookAuth),
    # my round
    url(r'^/rounds', views.myOpenRound),
    # age setting
    url(r'^', views.ageSetting)
]