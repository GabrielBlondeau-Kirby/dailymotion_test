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

    if not check_all_required_fields(fields, mandatory_fields):
        print(f"Failed : {fields} | {mandatory_fields}")
        return HttpResponseBadRequest(f"Missing field to create a user. One of {mandatory_fields}")

    # Create User
    user = User().create(body)

    # For Basic Auth
    DjUser.objects.create_user(body['email'], body['email'], body['password'], ).save()

    # Send 4 digit
    code, end = create_token(body["email"])

    user.update({"code": code, "code_end_on": end.timestamp()})

    return JsonResponse(user.to_json())


@api_view(["POST"])
def verify_user(request: Request):
    if not request.user.is_authenticated:
        print(f"{bcolors.FAIL}Code is wrong format{bcolors.ENDC}")
        return HttpResponseUnauthorized()

    mandatory_fields = ["digit_code"]
    body = request.data
    print(f"{bcolors.OKCYAN}User: {request.user}{bcolors.ENDC}")

    fields = body.keys()

    if not check_all_required_fields(fields, mandatory_fields):
        print(f"{bcolors.FAIL}Failed : {fields} | {mandatory_fields}{bcolors.ENDC}")
        return HttpResponseBadRequest(f"Digit code is missing")

    try:
        code = int(body['digit_code'])
        print(f"Code: {code} | {code.__class__}")
    except Exception as e:
        print(f"{bcolors.WARNING}Code is wrong format | error: {e}{bcolors.ENDC}")
        return HttpResponseBadRequest("Code is not is good format")

    user = User().get_by_email(str(request.user))    # request.user => email

    if code != user.code:
        print(f"{bcolors.WARNING}Code is wrong{bcolors.ENDC}")
        return HttpResponseBadRequest(f"Something is wrong with the token")

    if (user.code_end_on - datetime.today().timestamp()) < 1:
        print(f"{bcolors.WARNING}Timeout{bcolors.ENDC}")
        return HttpResponseBadRequest(f"Token timeout")

    user.update({"status": "active", "is_verified": True})

    return JsonResponse(user.to_json())


@api_view(["GET"])
def refresh_token(request: Request):
    user = User().get_by_email(str(request.user))    # request.user => email

    code, end = create_token(user.email)

    user.update({"code": code, "code_end_on": end.timestamp()})

    return JsonResponse({"digit_code": code})


def create_token(email: str) -> (int, datetime):
    # Send 4 digit
    code = CodeSecure().send_digit_code(email, code_type="4digit", timeout_seconds=60)
    end = datetime.today() + timedelta(minutes=1)
    print(f"{bcolors.OKBLUE} New code: {code} | {bcolors.OKCYAN}end at: {end}{bcolors.ENDC}")
    return code, end
