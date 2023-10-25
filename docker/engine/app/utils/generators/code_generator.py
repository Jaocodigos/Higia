import random
import string


def generate_code(code_size: int, types=None):
    char_types = None
    if types:
        for t in types:
            char_types = char_types + t
    else:
        char_types = string.ascii_letters + string.digits
    code = ''.join(random.choice(char_types) for _ in range(code_size))
    return code
