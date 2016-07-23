from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from utils import createResponseData


"""
* Round
"""
@api_view(['GET'])
def getRound(request):
    if request.method == 'GET':  # 더미
        data = {
            "id": 1,
            "question": "불라불라",
            "create_date": "2016-07-24",
            "member": 130
        }
        return Response(createResponseData(0, "success", data))


@api_view(['POST'])
def postRound(request):
    if request.method == 'POST':  # 더미
        return Response(createResponseData(0, "success", None))


@api_view(['PUT', 'DELETE'])
def round(request, round_id):
    if request.method == 'PUT':  # 더미
        return Response(createResponseData(0, "success", None))
    if request.method == 'DELETE':  # 더미
        return Response(createResponseData(0, "success", None))


@api_view(['POST'])
def pick(request):
    if request.method == 'POST':  # 더미
        return Response(createResponseData(0, "success", None))


@api_view(['GET'])
def backgroundImage(request):
    data = [
        {"id": 1, "image": "이미지 URL"},
        {"id": 2, "image": "이미지 URL"}
    ]
    if request.method == 'GET':  # 더미
        return Response(createResponseData(0, "success", data))

"""
* Comment
"""
@api_view(['GET'])
def commentList(request, round_id):
    if request.method == 'GET':  # 더미
        data = [
            {"id": 1, "content": "댓글어쩌구저쩌구", "create_date": "2016-07-25", "like": 100},
            {"id": 2, "content": "댓글어쩌구", "create_date": "2016-07-24", "like": 50}
        ]
        return Response(createResponseData(0, "success", data))


@api_view(['POST'])
def postComment(request):
    if request.method == 'POST':  # 더미
        return Response(createResponseData(0, "success", None))


@api_view(['PUT', 'DELETE'])
def comment(request, comment_id):
    if request.method == 'PUT':  # 더미
        return Response(createResponseData(0, "success", None))
    if request.method == 'DELETE':  # 더미
        return Response(createResponseData(0, "success", None))


"""
* Recomment
"""
@api_view(['GET'])
def recommentList(request, comment_id):
    if request.method == 'GET':  # 더미
        data = [
            {"id": 3, "content": "대댓글어쩌구저쩌구", "create_date": "2016-07-25", "like": 100, "comment_id": 1},
            {"id": 4, "content": "대댓글어쩌구", "create_date": "2016-07-24", "like": 50, "comment_id":1}
        ]
        return Response(createResponseData(0, "success", data))


@api_view(['POST'])
def postRecomment(request):
    if request.method == 'POST':  # 더미
        return Response(createResponseData(0, "success", None))


@api_view(['PUT', 'DELETE'])
def recomment(request, recomment_id):
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
@api_view(['GET'])
def myOpenRound(request):
    if request.method == 'GET':  # 더미
        data = [
            {"id": 1, "question": "불라불라", "create_date": "2017-07-25", "member": 130, "complete": 0},
            {"id": 2, "question": "불라불라1234", "create_date": "2017-07-25", "member": 10, "complete": 2}
        ]
        return Response(createResponseData(0, "success", data))


@api_view(['GET'])
def myPickRound(request):
    if request.method == 'GET':  # 더미
        data = [
            {"id": 1, "question": "불라불라", "create_date": "2017-07-25", "member": 130, "complete": 0},
            {"id": 2, "question": "불라불라1234", "create_date": "2017-07-25", "member": 10, "complete": 2}
        ]
        return Response(createResponseData(0, "success", data))