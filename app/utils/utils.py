import random
import string

def generate_random_id(length: int = 15):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
