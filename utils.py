import re
import hashlib
import os.path, os


# To print colors in terminal
class COLOR:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def replace_i(text, old, new):
    match = re.compile(re.escape(old), re.IGNORECASE)
    return match.sub(new, text)

def insert_sorted(array, element):
    n = len(array)
    for i in range(n):
        if element < array[i]:
            array.insert(i, element)
            return
        elif element == array[i]:
            return
    array.append(element)

def hash_file(filepath):
    BUF_SIZE = 65536  # 64kb chunks
    sha1 = hashlib.sha1()

    with open(filepath, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)

    return sha1.hexdigest()

if not os.path.exists('__cache__'):
    os.makedirs('__cache__')