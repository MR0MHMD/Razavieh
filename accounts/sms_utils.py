from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from .models import CustomUser
import requests
import random
import json


def send_otp_via_ghasedak(phone_number, code):
    url = "https://gateway.ghasedak.me/rest/api/v1/WebService/SendOtpSMS"

    payload = json.dumps({
        "sendDate": timezone.now().isoformat(),
        "receptors": [
            {
                "mobile": phone_number,
                "clientReferenceId": "1"
            }
        ],
        "templateName": "Authrazaviyeh",
        "inputs": [
            {
                "param": "Code",
                "value": code
            }
        ],
        "udh": True
    })
    headers = {
        'Content-Type': 'application/json',
        'ApiKey': settings.GHASEDAK_API_KEY
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def generate_otp():
    return f"{random.randint(100000, 999999)}"


def send_verification_code(user: CustomUser):
    code = generate_otp()
    user.verification_code = code
    user.otp_created_at = timezone.now()
    user.save(update_fields=['verification_code', 'otp_created_at'])
    response = send_otp_via_ghasedak(user.phone_number, code)
    return response


def verify_otp(user: CustomUser, code: str):
    if user.verification_code != code:
        return False, "کد اشتباه است"

    # بررسی محدودیت 2 دقیقه
    if user.otp_created_at and timezone.now() > user.otp_created_at + timedelta(minutes=2):
        return False, "کد منقضی شده است"

    # پاک کردن OTP بعد از تایید
    user.verification_code = ""
    user.otp_created_at = None
    user.save(update_fields=['verification_code', 'otp_created_at'])
    return True, "کد صحیح است"
