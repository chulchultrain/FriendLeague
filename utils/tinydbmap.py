import tinydb

class TinyDBMap:
    def __init__(self,base_file,key_field):
        self._data = tinydb.TinyDB(base_file)
        self._key = key_field
        self._length = len(self._data.all())

    def __contains__(self,key):
        with_key = self._data.search(tinydb.where(self._key) == key)
        return len(with_key) > 0

    def __delitem__(self,key):
        if key in self:
            self._data.remove(tinydb.where(self._key) == key)
            self._length -= 1

    def __getitem__(self,key):
        li = self._data.search(tinydb.where(self._key) == key)
        if len(li) == 0:
            raise KeyError("missing key " + str(key))
        elif len(li) > 1:
            raise Exception("too many values with key " + str(key))
        else:
            return li[0]

    def __setitem__(self,key,value):
        value[self._key] = key
        if key in self:
            del self[key]
        else:
            self._length += 1
        self._data.insert(value)

    def __iter__(self):
        res = []
        for f in self._data:
            res.append(f[self._key])
        return iter(res)

def testing():
    db = TinyDBMap("db.json","id")
    store_thing = {'name':'grapes of wrath'}
    store_thing_2 = {'name':'herpes'}
    db[1] = store_thing
    db[2] = store_thing_2
    for f in db:
        print(db[f])
    del db[1]
    for f in db:
        print(db[f])
    if 1 in db:
        print(db[1])
    if 2 in db:
        print(db[2])

if __name__ == "__main__":
    testing()
