from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from rest_framework.decorators import api_view
from .codeSecure_service import CodeSecure
from .tools import check_all_required_fields, bcolors
from .models import User
from datetime import datetime, timedelta


@api_view(["GET"])
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@api_view(["POST"])
def create_user(request):
    """
    POST /users/create

    :param request: None
    :return:
    """
    # make sure all fields are defined

    body = request.data

    fields = body.keys()

    mandatory_fields = ["email", "password"]

    if not check_all_required_fields(fields, mandatory_fields):
        print(f"Failed : {fields} | {mandatory_fields}")
        return HttpResponseBadRequest(f"Missing field to create a user. One of {mandatory_fields}")

    # Create User
    user = User().create(body)
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
def verify_user(request):
    mandatory_fields = ["digit_code"]

    body = request.data

    fields = body.keys()

    if not check_all_required_fields(fields, mandatory_fields):
        print(f"Failed : {fields} | {mandatory_fields}")
        return HttpResponseBadRequest(f"Digit code is missing")

    resp = {"test": 42}

    return JsonResponse(resp)
