class Hash:     # use Hash[x] to hash
    def __init__(self, _bucket_size, _hasher=hash):
        self.__bucket_size = _bucket_size
        self.__hasher = _hasher
    def __getitem__(self, _key):
        return self.__hasher(_key) % self.__bucket_size

class HashTable:
    def __init__(self, _bucket_size, _hasher=Hash):
        self.__bucket_size = _bucket_size
        self.__hasher = _hasher(_bucket_size)
        self.__bucket = [[] for i in range(_bucket_size)]
    def count_key(self, _key) -> bool:
        return _key in self.__bucket[self.__hasher[_key]]
    def find_key(self, _key) -> tuple:
        key = self.__hasher[_key]
        if not self.count_key(_key):
            return -1, -1
        id = 0
        while (not self.__bucket[key][id] == _key) and (id < len(self.__bucket[key])):
            id += 1
        return key, id
    def add_key(self, _key) -> bool:
        if _key == None:
            raise KeyError('Key in HashTable can not be None')
        if not self.count_key(_key):
            self.__bucket[self.__hasher[_key]].append(_key)
            return True
        return False
    def erase_key(self, _key) -> bool:
        if not self.count_key(_key):
            return False
        key, id = self.find_key(_key)
        del self.__bucket[key][id]
        return True
    def hash(self, _key):
        return self.__hasher[_key]
    def hasher(self):
        return self.__hasher
    def bucket_size(self) -> int:
        return self.__bucket_size
    def bucket(self):
        return self.__bucket
    def table_size(self) -> int:
        _table_size = 0
        for i in self.__bucket:
            _table_size += len(i)
        return _table_size
    def count_bucket(self, _key=None) -> int:
        ret = 0
        for i in self.__bucket:
            if not len(i) == 0:
                ret += 1
            if _key in i:
                break
        return ret
    def find_first_key(self):
        _key = 0
        while _key < self.__bucket_size:
            if not len(self.__bucket[_key]) == 0:
                break
            _key += 1
        return self.__bucket[_key][0]
    def find_last_key(self):
        _key = self.__bucket_size-1
        while _key >= 0:
            if not len(self.__bucket[_key]) == 0:
                break
            _key -= 1
        return self.__bucket[_key][-1]
    def find_next_key(self, key):
        if key == None:
            return None
        _key, _id = self.find_key(key)
        if not _id+1 == len(self.__bucket[_key]):
            return self.__bucket[_key][_id+1]
        _key += 1
        while _key < self.__bucket_size:
            if not len(self.__bucket[_key]) == 0:
                break
            _key += 1
        if _key == self.__bucket_size:
            return None
        return self.__bucket[_key][0]
    def find_prev_key(self, key):
        if key == None:
            return None
        _key, _id = self.find_key(key)
        if not _id-1 == -1:
            return self.__bucket[_key][_id-1]
        _key -= 1
        while _key >= 0:
            if not len(self.__bucket[_key]) == 0:
                break
            _key -= 1
        if _key == -1:
            return None
        return self.__bucket[_key][-1]
    def get_keys(self) -> list:
        ret, key = [], self.find_first_key()
        while not key == None:
            ret.append(key)
            key = self.find_next_key(key)
        return ret
    def clear_table(self):
        self.__bucket.clear()

HASHMAP_DEFAULT_BUCKET_SIZE = int(3e5)

class HashMap(HashTable):
    def __init__(self, _bucket_size=HASHMAP_DEFAULT_BUCKET_SIZE, _hasher=Hash):
        super().__init__(_bucket_size, _hasher)
        self.__value = [[] for i in range(_bucket_size)]
    def insert(self, _pair) -> bool:
        _key, _val = _pair
        if not self.add_key(_key):
            return False
        key, id = self.find_key(_key)
        self.__value[key].insert(id, _val)
        return True
    def emplace(self, _key, _val) -> bool:
        return self.insert((_key, _val))
    def erase(self, _key) -> bool:
        if not self.count_key(_key):
            return False
        key, id = self.find_key(_key)
        self.erase_key(_key)
        del self.__value[key][id]
    def size(self) -> int:
        return self.table_size()
    def fix(self) -> bool:
        bkt = self.bucket()
        ret = False
        for i in range(self.bucket_size()):
            while not len(self.__value[i]) == len(bkt[i]):
                ret = True
                self.__value[i].append(None)
        return ret
    def clear(self):
        self.clear_table()
        self.__value.clear()
    def __setitem__(self, _key, _val):
        if not self.count_key(_key):
            self.insert((_key, _val))
        key, id = self.find_key(_key)
        self.__value[key][id] = _val
        return _val
    def __getitem__(self, _key):
        key, id = self.find_key(_key)
        if key == -1 and id == -1:
            raise KeyError('Key is not found in this HashMap')
        return self.__value[key][id]
    def __delitem__(self, _key):
        self.erase(_key)
    def __contains__(self, _key):
        return self.count_key(_key)
    def __len__(self):
        return self.size()
    def count(self, _key):
        return self.count_key(_key)
    def __iter__(self):
        key = self.find_first_key()
        while not key == None:
            yield key
            key = self.find_next_key(key)
    def __str__(self):
        ret = '{\n'
        for i in self.get_keys():
            key, id = self.find_key(i)
            ret += ' ' + str(i) + ': ' + str(self.__value[key][id]) + ',\n'
        ret = ret[:-2] + '\n}'
        return ret

HASHSET_DEFAULT_BUCKET_SIZE = int(3e5)

class HashSet(HashTable):
    def __init__(self, _bucket_size=HASHSET_DEFAULT_BUCKET_SIZE, _hasher=Hash):
        super().__init__(_bucket_size, _hasher)
    def insert(self, _key) -> bool:
        return self.add_key(_key)
    def emplace(self, _key) -> bool:
        return self.add_key(_key)
    def erase(self, _key) -> bool:
        return self.erase_key(_key)
    def count(self) -> bool:
        return self.count()
    def find(self, _key) -> int:
        key, id = self.find_key(_key)
        if key == -1:
            return None
        cbk = self.count_bucket(_key)
        return cbk+id-1
    def size(self):
        return self.table_size()
    def elemens(self):
        return self.get_keys()
    def union(self, o: object):
        if not type(self) == type(o):
            raise TypeError('Argument type must be HashSet')
        for i in o.get_keys():
            self.add_key(i)
    def subtract(self, o: object):
        if not type(self) == type(o):
            raise TypeError('Argument type must be HashSet')
        for i in o.get_keys():
            self.erase_key(i)
    def intersect(self, o: object):
        if not type(self) == type(o):
            raise TypeError('Argument type must be HashSet')
        for i in self.get_keys():
            if not o.count_key(i):
                self.erase_key(i)
    def clear(self):
        self.clear_table()
    def __len__(self):
        return self.table_size()
    def __delitem__(self, _key):
        self.erase_key(_key)
    def __contains__(self, _key):
        return self.count_key(_key)
    def __iter__(self):
        key = self.find_first_key()
        while not key == None:
            yield key
            key = self.find_next_key(key)
    def __str__(self):
        ret = str(self.get_keys())
        ret = '{' + ret[1:-1] + '}'
        return ret