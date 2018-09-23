
import sys
import pickle
import os

#potential problem: overload a single directory with alot of files, if there are alot of keys
#potential solution: create load balancing with subdirectories.
#potential problem: lots of file accesses due to there being so many files still(not as bad as above, but still alot)
#potential problem: merge a few into a single file

class Filemap:

    def __init__(self,dir=''):
        self.set_dir(dir)


    def set_dir(self,dir):
        self._base_dir = dir
        self._create_base_dir()
        
    def __setitem__(self,key,value):
        self._write_item(key,value)

    def _create_base_dir(self):
        if os.path.isdir(self._base_dir) is False:
            os.makedirs(self._base_dir)

    def __getitem__(self,key):
        return self._read_item(key)

    def _get_file_name(self,key):
        return self._base_dir + '/' + str(key)

    def _write_item(self,key,value):
        try:
            with open(self._get_file_name(key),'wb') as fout:
                pickle.dump(value,fout)
        except Exception as e:
            print("Couldn't write pickled file")
            print(e)
    def _read_item(self,key):
        res = None
        try:
            with open(self._get_file_name(key),'rb') as fin:
                res = pickle.load(fin)
        except Exception as e:
            print("Couldn't load pickled file ")
            print(e)
            res = None
        return res

    def __iter__(self):
        res = []
        try:
            res = set(os.listdir(self._base_dir))
        except Exception as e:
            print(e)
        return iter(res)

    def __contains__(self,item):
        try:
            files = os.listdir(self._base_dir)
        except Exception as e:
            print(e)
        return str(item) in files


def test_set():
    fm = Filemap('data')
    d = {}
    d['asdf'] = 'herp'
    d[1] = 'derp'
    fm['d'] = d

def test_get():
    fm = Filemap('data')
    r = fm['d']
    #print(r)
    for x in r:
        print(str(x) + ' ' + r[x])

def test_iter():
    fm = Filemap('data')
    for f in fm:
        print(f)

def test_contains():
    fm = Filemap('data')
    print('d' in fm)
    print('a' in fm)

if __name__ == '__main__':
    test_set()
    test_get()
    test_iter()
    test_contains()
