import lib.HashContainer as hc
import random
import time


class hasher(hc.Hash):
    def __init__(self, bucket_size):
        def hash_function(key):
            ret = 0
            for i in key:
                ret = ret*10 + ord(i)
            return ret
        super().__init__(bucket_size, hash_function)

mp = hc.HashMap(hc.HASHMAP_DEFAULT_BUCKET_SIZE, hasher)
keys = []
res = []
n = 100000

start = time.monotonic()
for i in range(n):
    keys.append('')
    for i in range(8):
        keys[-1] += (chr(random.randint(65, 120)))

for i in range(n):
    mp[keys[i]] = i

print(len(mp))
res.append(time.monotonic()-start)

'''
mp = {}

start = time.monotonic()
for i in range(n):
    mp[keys[i]] = i

print(mp)
print(len(mp))
res.append(time.monotonic()-start)
'''

print(res)
print(mp.count_bucket())