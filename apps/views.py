from random import randint

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import DestroyModelMixin

from utils import createResponseData, baseURL
from .exceptions import NoYesOrNoException
from .exceptions import BadRequestException
from .models import BackgroundImage
from .models import Comment
from .models import CommentLike
from .models import Pick
from .models import Round
from .serializers import CommentSerializer, RecommentSerializer
from .serializers import MyRoundSerializer
from .serializers import PickSerializer
from .serializers import RoundSerializer
from .serializers import CommentLikeSerializer


"""
* Round
"""
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def round(request):

    # GET method와 POST method 에서 처리하는 로직이 상이하다.
    # POST method에서 처리하는 로직은, DRF가 제공하는 CreateAPIView를 잘 활용할 수 있다.
    # GET method는 FBV로 직접 구현해야 할 것이다.
    # 상이한 로직이 하나의 URI에 묶여있으므로 분기해야한다.
    # view에서 다른 view들을 감싸는 방법에 대해서는 스택오버플로우 링크를 참고함
    # http://stackoverflow.com/questions/14956678/django-call-class-based-view-from-another-class-based-view

    if request.method == 'GET':
        random_round = Round.objects.get_random()
        data = [
            {
                "id": random_round.id,
                "question": random_round.question,
                "create_date": random_round.create_date,
                "member": random_round.get_member(),
                "comment": Comment.objects.filter(pick__round=random_round).count()
            }
        ]
        # return Response(createResponseData(0, "success", data))
        return Response(data)
    if request.method == 'POST':
        return RoundCreate.as_view()(request)


class RoundCreate(CreateAPIView):
    serializer_class = RoundSerializer


@api_view(['PUT', 'DELETE'])
def editRound(request, round_id):
    if request.method == 'PUT':  # 더미
        return Response(createResponseData(0, "success", None))
    if request.method == 'DELETE':  # 더미
        return Response(createResponseData(0, "success", None))


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
@transaction.atomic
def pick(request):
    if request.method == 'GET':  # 더미
        picks_round = Pick.objects.filter(user=request.user)
        picks_round_list = []
        for cnt, pick in enumerate(picks_round):
            picks_round_list.append({})
            picks_round_list[cnt]['id'] = pick.round.id
            picks_round_list[cnt]['question'] = pick.round.question
            picks_round_list[cnt]['yes_no'] = int(pick.yes_no)
            picks_round_list[cnt]['create_date'] = pick.round.create_date
            picks_round_list[cnt]['member'] = pick.round.get_member()
            picks_round_list[cnt]['complete'] = pick.round.complete
        return Response(picks_round_list)
    if request.method == 'POST':
        serializer = PickSerializer(data=request.data)
        if serializer.is_valid():
            try:
                Pick.objects.get(user=request.user, round_id=request.data["round"])
                raise BadRequestException("You already pick the round.")
            except ObjectDoesNotExist:
                nickname_id = Pick.objects.next_nickname_id(request.data['round'])
                serializer.save(user=request.user, nickname_id=nickname_id)
                return Response(data=serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def backgroundImage(request):
    if request.method == 'GET':
        imgViewerURL = baseURL() + "image/"  # 이미지 경로 만들기
        bg_data = BackgroundImage.objects.filter(is_active=True).values('id', 'image')
        for bg in bg_data:
            bg['image'] = imgViewerURL + str(bg['image'])
        return Response(bg_data)


@api_view(['GET'])
def imageViewer(request, img):
    img_path = settings.STATIC_ROOT + '\\images\\' + img
    bgimg = open(img_path, 'rb')
    return HttpResponse(bgimg.read(), content_type="image/jpg")


"""
* Comment
"""
class CommentListCreate(ListCreateAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    serializer_class = CommentSerializer

    # Comment의 목록을 필터링해줄 queryset을 반환하는 get_queryset을 오버라이딩.
    # URI에서 round_id 값을 뽑아서, 해당 Round에 달린 comment 정보만 반환한다.
    # URI GET parameter에서 yes_no 값을 뽑아서, 해당 진영의 comment 정보만 반환한다.
    def get_queryset(self):
        return Comment.objects.filter(
            pick__round_id=self.kwargs["round_id"],
            pick__yes_no=self.request.GET.get("yes_no"),
            parent=None
        )

    # GET 요청에 "yes_no" params가 없는 경우에 대한 에러처리를 위해 list를 오버라이딩
    def list(self, request, *args, **kwargs):
        try:
            # "yes_no" 가 없으면 에러 발생
            assert self.request.GET.get("yes_no") is not None
            return super(CommentListCreate, self).list(request, *args, **kwargs)
        except AssertionError:
            raise NoYesOrNoException()


@api_view(['PUT', 'DELETE'])
def editComment(request, comment_id):
    if request.method == 'PUT':  # 더미
        return Response(createResponseData(0, "success", None))
    if request.method == 'DELETE':  # 더미
        return Response(createResponseData(0, "success", None))


"""
* Recomment
"""
class RecommentListCreate(ListCreateAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    serializer_class = RecommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(parent_id=self.kwargs["comment_id"], is_active=1)


@api_view(['PUT', 'DELETE'])
def editRecomment(request, recomment_id):
    if request.method == 'PUT':  # 더미
        return Response(createResponseData(0, "success", None))
    if request.method == 'DELETE':  # 더미
        return Response(createResponseData(0, "success", None))


"""
* Like
"""
@api_view(['POST'])
def likeUp(request):
    if request.method == 'POST':  # 더미
        return Response(createResponseData(0, "success", None))


@api_view(['DELETE'])
def likeDown(request, id):
    if request.method == 'DELETE':  # 더미
        return Response(createResponseData(0, "success", None))


"""
* My Round
"""
class MyRoundList(ListAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    serializer_class = MyRoundSerializer

    # 자신이 생성한 라운드들만 받아오도록 get_queryset 메소드를 오버라이딩
    def get_queryset(self):
        user = self.request.user
        return Round.objects.filter(user=user)


class CommentLikeCreateDestroy(CreateModelMixin, DestroyModelMixin, GenericAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    serializer_class = CommentLikeSerializer

    # get_queryset 메소드와 get_object 메소드의 역할 구분에 대해서는 헷갈리는 부분.
    def get_queryset(self):
        return get_object_or_404(
            CommentLike,
            user=self.request.user,
            comment_id=self.kwargs["comment_id"]
        )

    def get_object(self):
        return self.get_queryset()

    # CreateAPIView 의 내용을 가져옴.
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # DestroyAPIView 의 내용을 가져옴.
    def delete(self, request, *args, **kwargs):
        # 해당 Comment의 like 필드값을 1 감소시킨다.
        Comment.objects.filter(id=self.get_object().comment_id).update(like=F("like")-1)
        return self.destroy(request, *args, **kwargs)
