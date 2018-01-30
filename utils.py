import re
import hashlib
import os.path
import os
import sys
import pickle
from zipfile import ZipFile
from urllib.request import urlretrieve
# project
import words


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

def add_line_str(content, line):
    if content is not None:
        content += "\n" + line
    else:
        content = line
    return content

def highlighted_content(document, query, color=COLOR.BOLD):
    content = document.content
    url = document.url
    if (content is None) and (url is not None):
        with open(url, 'r') as opened:
            content = opened.read()
    elif content is None and url is None:
        return ""
    query = query.replace('&', ' ')
    query = query.replace('|', ' ')
    query = query.replace('~', ' ')
    query_terms = set(words.process(query, terms_only=True))
    tokens = words.tokenize(content, lower=False)
    for token in tokens:
        term = words.process(token.lower(), terms_only=True)[0]
        if term in query_terms:
            replacement = "{}{}{}".format(color, token, COLOR.ENDC)
            content = content.replace(token, replacement)
    return content

def hash_collection(path):
    hashed = hashlib.sha1((path + str(os.path.getsize(path))).encode())
    return hashed.hexdigest()

CACHE_DIR = 'dumps'
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def get_cache(cachefile):
    cachefile = os.path.join(CACHE_DIR, cachefile)
    if os.path.exists(cachefile):
        with open(cachefile, 'rb') as cache:
            try:
                return pickle.load(cache)
            except pickle.UnpicklingError:
                pass
    return None

def set_cache(cachefile, obj):
    cachefile = os.path.join(CACHE_DIR, cachefile)
    with open(cachefile, 'wb') as cache:
        pickle.dump(obj, cache)

def download_collection(url):
    path = os.path.join(CACHE_DIR, os.path.basename(url))
    download(url, path)
    splitext = os.path.splitext(os.path.basename(path))
    if splitext[1] == '.zip':
        dest = os.path.join(CACHE_DIR, splitext[0])
        extract_zip(path, dest)
        return dest
    return path

def download(url, path):
    if not os.path.exists(path):
        sys.stderr.write("downloading %s\n" % url)
        urlretrieve(url, path, reporthook)

def reporthook(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        sys.stderr.write("\r%5.1f%% %*d / %d" % (
            percent, len(str(totalsize)), readsofar, totalsize))
        if readsofar >= totalsize:
            sys.stderr.write("\n")
    else:
        sys.stderr.write("read %d\n" % (readsofar,))

def extract_zip(filepath, destpath):
    if os.path.exists(destpath):
        return
    sys.stderr.write("extracting %s\n" % (os.path.basename(filepath)))
    with ZipFile(filepath) as openedzip:
        openedzip.extractall(path=destpath)

def is_url(string):
    pattern = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return pattern.match(string) is not None
