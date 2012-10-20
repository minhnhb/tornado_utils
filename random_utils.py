import string
import random

def rand_string(size=6, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for x in range(size))


def rand_ascii(size=6):
    return rand_string(size, string.ascii_uppercase + string.ascii_letters)

def rand_int(size=6):
    return rand_string(size, string.digits)

if __name__ == '__main__':
    print rand_string(8)
    print rand_int()
