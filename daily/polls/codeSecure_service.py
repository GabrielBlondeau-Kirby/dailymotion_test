from random import randrange
from django.test.client import RequestFactory

from .tools import bcolors

CODE_SECURE_API_KEY = "my_api_key"


class CodeSecure:

    def __init__(self):
        self.api_key = CODE_SECURE_API_KEY
        self.origin_url = "www.code_secure_api.com"

    def send_digit_code(self, email: str, code_type: str = "4digit", timeout_seconds: int = 60):
        endpoint = "email-code"
        try:
            print(f"{bcolors.OKBLUE}sending 4 digit to {email} | code type: {code_type}{bcolors.ENDC}")
            print(f"email has been sent")
            digit = randrange(1000, 9999)
            print(f"{bcolors.OKGREEN}digit: {digit} {bcolors.ENDC}")
            return digit

            # if response.status_code == 200:
            #     return digit
            # else:
            #     print(f"[CodeSecure] Error while sending email | email: {email} | status: {response.status_code}")
            #     raise Exception(f"Sending Code failed")
        except Exception as e:
            print(f"Sending email process failed | error: {e}")
            raise e
