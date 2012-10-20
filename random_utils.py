import string
import random

def rand_string(size=6, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for x in range(size))

if __name__ == '__main__':
    print rand_string(8)
