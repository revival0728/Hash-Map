#include <functional>
#include <utility>
#include <vector>

namespace hashmap {
    using size_t = unsigned int;
    template <class Key, class Value, class _Hasher=std::hash<Key>, class Key_Container=std::vector<Key>, class Value_Container=std::vector<Value>>
    class HashMap {
        protected:
        friend class iterator;

        std::vector<Key_Container> key;
        std::vector<Value_Container> val;
        size_t _bucket_size;

        public:
        HashMap(size_t __bucket_size) : _bucket_size(__bucket_size) {
            key = std::vector<Key_Container>(_bucket_size);
            val = std::vector<Value_Container>(_bucket_size);
        }
        ~HashMap() {}

        class Hasher {
            _Hasher _hsr;
            size_t _bks;

            public:
            Hasher(size_t __bks) : _bks(__bks) {}
            Hasher(const Hasher& __hasher) {*this = __hasher;}
            size_t operator()(Key _key) {return _hsr(_key) % _bks;}
        };

        protected:
        Hasher hsr = Hasher(_bucket_size);

        std::pair<size_t, size_t> _find(Key _key) {
            size_t _id = 0, _hash = hsr(_key);
            for(; _id < key[_hash].size(); ++_id)
                if(key[_hash][_id] == _key) break;
            return {_hash, _id};
        }

        public:
        class iterator {
            template <class T>
            using _iterator = typename std::vector<T>::iterator;

            size_t hash_id;
            std::pair<_iterator<Key>, _iterator<Value>> p;
            HashMap<Key, Value> *mp;
            
            friend class HashMap;
            public:
            iterator(HashMap<Key, Value> *_mp, _iterator<Key>& _key, _iterator<Value>& _val, size_t _hash) {
                hash_id = _hash;
                mp = _mp;
                p = {_key, _val};
            }
            iterator(const iterator& it) {*this = it;}
            iterator(HashMap<Key, Value> *_mp, size_t _hash, size_t _id) {
                hash_id = _hash;
                mp = _mp;
                p = {mp->key[_hash].begin()+_id, mp->val[_hash].begin()+_id};
            }
            ~iterator() {}
            iterator operator++() {
                ++p.first, ++p.second;
                if(p.first != mp->key[hash_id].end() || hash_id == mp->key.size()-1)
                    return *this;
                while(p.first == mp->key[hash_id].end() || mp->key[hash_id].size() == 0) {
                    if(hash_id == mp->key[hash_id].size()-1)
                        break;
                    ++hash_id;
                }
                p.first = mp->key[hash_id].begin();
                p.second = mp->val[hash_id].begin();
                return *this;
            }
            iterator operator++(int) {iterator it=iterator(*this); operator++(); return it;}
            iterator operator--() {
                if(p.first != mp->key[hash_id].begin() || hash_id == 0) {
                    --p.first, --p.second;
                    return *this;
                }
                while(p.first == mp->key[hash_id].begin() || mp->key[hash_id].size() == 0) {
                    if(hash_id == 0)
                        break;
                    --hash_id;
                }
                if(mp->key[hash_id].size() == 0) {
                    p.first = mp->key[hash_id].end();
                    p.second = mp->val[hash_id].end();
                } else {
                    p.first = mp->key[hash_id].end()-1;
                    p.second = mp->val[hash_id].end()-1;
                }
                return *this;
            }
            iterator operator--(int) {iterator it=iterator(*this); operator--(); return it;}
            _iterator<Key> get_key() {return p.first;}
            _iterator<Value> get_value() {return p.second;}
            std::pair<Key, Value> operator*() const {return {*p.first, *p.second};}

            friend bool operator==(const iterator lt, const iterator rt) {return lt.p == rt.p;}
            friend bool operator!=(const iterator lt, const iterator rt) {return lt.p != rt.p;}
        };
        iterator begin() {
            size_t _hash = 0;
            while(key[_hash].size() == 0 && _hash+1 < key.size()) ++_hash;
            return iterator(this, _hash, 0);
        }
        iterator end() {return iterator(this, _bucket_size-1, key[_bucket_size-1].size());}

        std::pair<iterator, bool> emplace(Key _key, Value _val) {
            auto pos = _find(_key);
            size_t _hash = pos.first, _id = pos.second;
            if(_id == key[_hash].size()) {
                key[_hash].push_back(_key);
                val[_hash].push_back(_val);
                return {iterator(this, _hash, _id), true};
            }
            return {iterator(this, _hash, _id), false};
        }
        std::pair<iterator, bool> insert(std::pair<Key, Value> _kv) {return emplace(_kv.first, _kv.second);}
        bool erase(Key _key) {
            auto pos = _find(_key);
            size_t _hash = pos.first, _id = pos.second;
            if(_id == key[_hash].size())
                return false;
            key[_hash].erase(key[_hash].begin()+_id);
            val[_hash].erase(val[_hash].begin()+_id);
            return true;
        }
        void erase(iterator it) {
            key[it.hash_id].erase(it.get_key());
            val[it.hash_id].erase(it.get_value());
        }
        Value& operator[](const Key _key) {
            auto ret = emplace(_key, Value());
            return *(ret.first.get_value());
        }
        iterator find(const Key _key) {
            auto pos = _find(_key);
            size_t _hash = pos.first, _id = pos.second;
            if(_id == key[_hash].size())
                return end();
            return iterator(this, _hash, _id);
        }
        size_t size() {
            size_t _size = 0;
            for(const auto& i : key)
                _size += i.size();
            return _size;
        }
        void clear() {*this = HashMap(_bucket_size);}
        size_t bucket(Key _key) {return hsr(_key);}
        size_t bucket_count() {
            size_t _bucket_count = 0;
            for(const auto& i : key)
                _bucket_count += (!i.empty());
            return _bucket_count;
        }
        size_t bucket_size() {return _bucket_size;}
        size_t count(Key _key) {return find(_key) != end();}
        bool empty() {return size() == 0;}
        Hasher hash_function() {return hsr;}

        friend bool operator==(const HashMap<Key, Value, _Hasher, Key_Container, Value_Container>& lmp,
                               const HashMap<Key, Value, _Hasher, Key_Container, Value_Container>& rmp) {
                                   return lmp.key == rmp.key && lmp.value == rmp.value && lmp._bucket_size == rmp._bucket_size;
                               }
        friend bool operator!=(const HashMap<Key, Value, _Hasher, Key_Container, Value_Container>& lmp,
                               const HashMap<Key, Value, _Hasher, Key_Container, Value_Container>& rmp) {
                                   !(lmp == rmp);
                               }
        friend void swap(const HashMap<Key, Value, _Hasher, Key_Container, Value_Container>& lmp,
                         const HashMap<Key, Value, _Hasher, Key_Container, Value_Container>& rmp) {
                             swap(lmp.key, rmp.key);
                             swap(lmp.val, rmp.val);
                             swap(lmp._bucket_size, rmp._bucket_size);
                             swap(lmp.hsr, rmp.hsr);
                         }
    };
}