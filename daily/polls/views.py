from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.models import User as DjUser

from rest_framework.decorators import api_view
from datetime import datetime, timedelta

from rest_framework.request import Request

from .codeSecure_service import CodeSecure
from .tools import check_all_required_fields, bcolors
from .models import User

class HttpResponseUnauthorized(HttpResponse):
    def __init__(self):
        super().__init__('401 Unauthorized', status=401)


@api_view(["GET"])
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@api_view(["POST"])
def create_user(request: Request):
    """
    POST /users/create

    :param request: None
    :return: JsonResponse
    """
    # make sure all fields are defined

    body = request.data
    fields = body.keys()
    mandatory_fields = ["email", "password"]

    print(f"Is authenticates: {request.user.is_authenticated}")

    return JsonResponse({42:42})

    if not check_all_required_fields(fields, mandatory_fields):
        print(f"Failed : {fields} | {mandatory_fields}")
        return HttpResponseBadRequest(f"Missing field to create a user. One of {mandatory_fields}")

    # Create User
    user = User().create(body)

    # For Basic Auth
    DjUser.objects.create_user(body['email'], body['email'], body['password'], ).save()

    print(user)

    # Send 4 digit
    code = CodeSecure().send_digit_code(body['email'], code_type="4digit", timeout_seconds=60)
    end = datetime.today() + timedelta(minutes=1)

    user.update({"code": code, "code_end_on": end.timestamp()})

    resp = {
        "user_id": user.uuid,
        "status": user.status,
        "debug": {
            "email": body["email"],
            "pw": body["password"],
            "user": user.to_json()
        },
    }

    return JsonResponse(resp)


@api_view(["POST"])
def verify_user(request: Request):
    if not request.user.is_authenticated:
        return HttpResponseUnauthorized()

    mandatory_fields = ["digit_code"]
    body = request.data
    print(f"{bcolors.OKCYAN}User: {request.user}{bcolors.ENDC}")
    # headers = request.headers

    fields = body.keys()

    if not check_all_required_fields(fields, mandatory_fields):
        print(f"Failed : {fields} | {mandatory_fields}")
        return HttpResponseBadRequest(f"Digit code is missing")

    code = body['digit_code']
    if not isinstance(code, int):
        return HttpResponseBadRequest("Code is not is good format")

    user = User().get_by_email(str(request.user))    # request.user => email

    if code != user.code:
        return HttpResponseBadRequest(f"Something is wrong with the token")

    if (user.code_end_on - datetime.today().timestamp()) < 1:
        return HttpResponseBadRequest(f"Token timeout")

    return JsonResponse(user.to_json())
