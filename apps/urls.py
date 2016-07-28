from django.conf.urls import url
from apps import views

urlpatterns = [
    # round
    url(r'^/rounds$', views.round),
    url(r'^/rounds/(?P<round_id>[0-9]+)$', views.editRound),
    url(r'^/picks$', views.pick),
    url(r'^/background-image$', views.backgroundImage),

    # comment
    url(r'^/rounds/(?P<round_id>[0-9]+)/comments$', views.CommentListCreate.as_view()),
    url(r'^/comments/(?P<comment_id>[0-9]+)$', views.editComment),

    # recomment
    url(r'^/comments/(?P<comment_id>[0-9]+)/recomments$', views.RecommentListCreate.as_view()),
    url(r'^/recomments/(?P<recomment_id>[0-9]+)$', views.editRecomment),

    # like
    url(r'^/likes$', views.likeUp),
    url(r'^/likes/(?P<id>[0-9]+)$', views.likeDown),

    # image viewer
    url(r'^/image/(?P<img>.*)$', views.imageViewer)
]