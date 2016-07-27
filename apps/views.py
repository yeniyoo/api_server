from django.conf import settings
from django.http import HttpResponse

from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils import createResponseData, baseURL
from .models import BackgroundImage
from .serializers import RoundSerializer


"""
* Round
"""
@api_view(['GET', 'POST'])
def round(request):
    if request.method == 'GET':  # 더미
        data = {
            "id": 1,
            "question": "불라불라",
            "create_date": "2016-07-24",
            "member": 130
        }
        return Response(createResponseData(0, "success", data))
    if request.method == 'POST':  # 더미
        return Response(createResponseData(0, "success", None))


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


class RoundCreate(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated]

    serializer_class = RoundSerializer
