import string
import random

def generate_captcha_text():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

