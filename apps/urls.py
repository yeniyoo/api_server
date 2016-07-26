from django.conf.urls import url
from apps import views

urlpatterns = [
    # recomment
    url(r'^/comments/(?P<comment_id>[0-9]+)/recomments', views.recomment),
    url(r'^/recomments/(?P<recomment_id>[0-9]+)', views.editRecomment),

    # comment
    url(r'^/rounds/(?P<round_id>[0-9]+)/comments', views.comment),
    url(r'^/comments/(?P<comment_id>[0-9]+)', views.editComment),

    # round
    url(r'^/rounds/(?P<round_id>[0-9]+)', views.editRound),
    url(r'^/rounds', views.round),
    url(r'^/picks', views.pick),
    url(r'^/background-image', views.backgroundImage),

    # like
    url(r'^/likes/(?P<id>[0-9]+)', views.likeDown),
    url(r'^/likes', views.likeUp)
]