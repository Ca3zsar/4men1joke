import json

import jwt
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from firebase_admin import db
from . import utils


@csrf_exempt
def register(request):
    if request.method == 'POST':
        response_data = {}
        info = json.loads(request.body)
        username = info.get("username", "")
        password = info.get("password", "")
        email = info.get("email", "")

        if username == "" or password == "" or email == "":
            return HttpResponse("Fields username, password and email must exist!", status=400)

        ref = db.reference('/users')
        ref1 = db.reference('/verification')

        if len(ref.order_by_child('username').equal_to(username).get().keys()) > 0:
            response_data["message"] = "There is a business rule that prevents you from creating that resource"
            response_data["reason"] = "name"
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=409)

        verification_code = utils.generateVerificationCode()

        jsonForRegister = {
            "username": username,
            "password": password,
            "email": email,
            "isVerified": 0
        }
        jsonForVerification = {
            "username": username,
            "verification_code": verification_code,
        }

        ref.push().set(jsonForRegister)
        ref1.push().set(jsonForVerification)

        utils.sendEmail(email, verification_code)

        response_data = {"message": f"Account successfully created!"}
        username = info.get("username", "")
        email = info.get("email", "")

        jwt_token = jwt.encode({'username': username, 'email': email}, 'secret', algorithm='HS256')
        response_data["token"] = jwt_token
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=201)
    else:
        return HttpResponse("Method not allowed", status=405)