import string
import random


def generate_verification_code():
    return '123321'

def generate_invite_code(length):
    chars = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(chars) for _ in range(length))
    return random_string