import hashlib
import requests
import collections
import io
import random

from functools import wraps


class Hasher(object):
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def __call__(self, file):
        hash = self.algorithm()
        with open(file, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), ''):
                hash.update(chunk)
        return hash.hexdigest()


md5 = Hasher(hashlib.md5)
sha1 = Hasher(hashlib.sha1)


def retry(count=5, exc_type=Exception):
    def decorator(func):
        @wraps(func)
        def result(*args, **kwargs):
            last_exc = None
            for _ in range(count):
                try:
                    return func(*args, **kwargs)
                except exc_type as e:
                    last_exc = e
                print("Retrying...")
            raise last_exc

        return result

    return decorator


@retry(3, Exception)
def might_fail():
    random_number = random.randint(0, 10)
    print('Got {}'.format(random_number))
    url = 'https://wontworklol' if random_number > 5 else 'https://google.com'
    requests.get(url)


might_fail()


class Cache:
    def __init__(self):
        self.memo = {}

    def store(self, fn):
        def wrapper(*args):
            if args not in self.memo:
                self.memo[args] = fn(*args)
            return self.memo[args]

        return wrapper

    def clear(self):
        self.memo.clear()


cache = Cache()


@cache.store
def somefct():
    return ""


cache.clear()

colors = ['blue', 'red', 'blue', 'yellow', 'blue', 'red']
counter = collections.Counter(colors)
print(counter.most_common()[0][0])

Point = collections.namedtuple('Point', ['x', 'y'])
p = Point(x=1, y=2)
print(p.x, p.y)
print(p._fields)
