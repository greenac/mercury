from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from user_handler import UserHandler
from response import Response

@csrf_exempt
def save_user(request):
    user_dict = None
    response = Response().USER_DOES_NOT_EXIST
    try:
        user_dict = json.loads(request.body)
    except Exception:
        response = Response().INCOMING_DATA_CORRUPTED
        pass
    if user_dict:
        user_handler = UserHandler(user_dict=user_dict)
        response = user_handler.save_user()
    return HttpResponse(json.loads({'response':response}))

@csrf_exempt
def get_user(request):
    user_dict = None
    response = Response().USER_DOES_NOT_EXIST
    user = {}
    try:
        user_dict = json.loads(request.body)
    except Exception:
        response = Response().INCOMING_DATA_CORRUPTED
        pass
    if user_dict:
        user_handler = UserHandler(user_dict=user_dict)
        user = user_handler.user_as_dict()
        response = user_handler.response_number
    return HttpResponse(json.loads({'response':response, 'user':user}))

