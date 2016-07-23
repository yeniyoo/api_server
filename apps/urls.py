from django.conf.urls import url
from apps import views

urlpatterns = [
    # round
    url(r'^get-round', views.getRound),
    url(r'^rounds/(?P<round_id>[0-9]+)', views.round),
    url(r'^rounds', views.postRound),
    url(r'^pick', views.pick),
    url(r'^background-image', views.backgroundImage),

    # comment
    url(r'^comments-list/(?P<round_id>[0-9]+)', views.commentList),
    url(r'^comments/(?P<comment_id>[0-9]+)', views.comment),
    url(r'^comments', views.postComment),

    # recomment
    url(r'^recomments-list/(?P<comment_id>[0-9]+)', views.recommentList),
    url(r'^recomments/(?P<recomment_id>[0-9]+)', views.recomment),
    url(r'^recomments', views.postRecomment),

    # like
    url(r'^like/(?P<id>[0-9]+)', views.likeDown),
    url(r'^like', views.likeUp),

    # my round
    url(r'^my-open-rounds', views.myOpenRound),
    url(r'^my-pick-rounds', views.myPickRound)
]