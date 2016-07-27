from random import randint

from django.conf import settings
from django.http import HttpResponse

from rest_framework.generics import CreateAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils import createResponseData, baseURL
from .models import BackgroundImage
from .models import Pick
from .models import Round
from .serializers import RoundSerializer


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

    if request.method == 'GET':  # 더미
        random_round = Round.objects.get_random()
        member = Pick.objects.get_member(random_round)
        data = {
            "id": random_round.id,
            "question": random_round.question,
            "create_date": random_round.create_date,
            "member": member,
        }
        # return Response(createResponseData(0, "success", data))
        return Response(data)
    if request.method == 'POST':
        return RoundCreate.as_view()(request)


@api_view(['PUT', 'DELETE'])
def editRound(request, round_id):
    if request.method == 'PUT':  # 더미
        return Response(createResponseData(0, "success", None))
    if request.method == 'DELETE':  # 더미
        return Response(createResponseData(0, "success", None))


@api_view(['GET', 'POST'])
def pick(request):
    if request.method == 'GET':  # 더미
        data = [
            {"id": 1, "question": "불라불라", "yes_no": 1, "create_date": "2017-07-25", "member": 130, "complete": 0},
            {"id": 2, "question": "불라불라1234", "yes_no": 0, "create_date": "2017-07-25", "member": 10, "complete": 2}
        ]
        return Response(createResponseData(0, "success", data))
    if request.method == 'POST':  # 더미
        return Response(createResponseData(0, "success", None))


@api_view(['GET'])
def backgroundImage(request):
    if request.method == 'GET':
        imgViewerURL = baseURL() + "image/"  # 이미지 경로 만들기
        bg_data = BackgroundImage.objects.filter(is_active=True).values('id', 'image')
        for bg in bg_data:
            bg['image'] = imgViewerURL + str(bg['image'])
        return Response(createResponseData(0, "success", bg_data))


@api_view(['GET'])
def imageViewer(request, img):
    img_path = settings.STATIC_ROOT + '\\images\\' + img
    bgimg = open(img_path, 'rb')
    return HttpResponse(bgimg.read(), content_type="image/jpg")


"""
* Comment
"""
@api_view(['GET', 'POST'])
def comment(request, round_id):
    if request.method == 'GET':  # 더미
        data = [
            {"id": 1, "content": "댓글어쩌구저쩌구", "create_date": "2016-07-25", "like": 100, "is_liked": True},
            {"id": 2, "content": "댓글어쩌구", "create_date": "2016-07-24", "like": 50, "is_liked": False}
        ]
        return Response(createResponseData(0, "success", data))
    if request.method == 'POST':  # 더미
        return Response(createResponseData(0, "success", None))


@api_view(['PUT', 'DELETE'])
def editComment(request, comment_id):
    if request.method == 'PUT':  # 더미
        return Response(createResponseData(0, "success", None))
    if request.method == 'DELETE':  # 더미
        return Response(createResponseData(0, "success", None))


"""
* Recomment
"""
@api_view(['GET', 'POST'])
def recomment(request, comment_id):
    if request.method == 'GET':  # 더미
        data = [
            {"id": 3, "content": "대댓글어쩌구저쩌구", "create_date": "2016-07-25", "like": 100, "is_liked": True, "comment_id": 1},
            {"id": 4, "content": "대댓글어쩌구", "create_date": "2016-07-24", "like": 50, "is_liked": False, "comment_id":1}
        ]
        return Response(createResponseData(0, "success", data))
    if request.method == 'POST':  # 더미
        return Response(createResponseData(0, "success", None))


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


class RoundCreate(CreateAPIView):
    serializer_class = RoundSerializer
