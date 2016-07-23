import requests


# Create response data
def createResponseData(code, msg, data):
    res_data = {"status": {"code": code, "message": msg}}
    if data is not None:
        res_data['data'] = data
    return res_data


# Facebook Graph api request
def fbGraphApi(access_token):
    graph_url = "https://graph.facebook.com/v2.7/me"
    params = {
        "access_token": access_token,
        "fields": "id,gender"  # 이메일, 핸드폰번호, 성별
    }
    # facebook graph api 요청
    response_data = requests.get(graph_url, params=params).json()
    return response_data