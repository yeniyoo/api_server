from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^facebook-auth', views.facebookAuth),
    url(r'^age', views.ageSetting)
]