import sqlite3
import pickle

class SqliteMap:
    def __init__(self,location):
        self._connection = sqlite3.connect(location,isolation_level=None)
        self._cursor = self._connection.cursor()
        self._cursor.execute('create table if not exists data_table ( key blob, value blob)' )
        self._cursor.execute('create unique index if not exists uni_index on data_table(key)')
    def __contains__(self,key):
        self._cursor.execute('select * from data_table where key=?',(key,))
        for f in self._cursor:
            return True
        return False
    def __getitem__(self,key):
        self._cursor.execute('select value from data_table where key=?',(key,))
        oneval = self._cursor.fetchone()
        if oneval is None:
            raise KeyError("missing key " + str(key))
        else:
            res = pickle.loads(str(oneval[0]))
            return res
    def __delitem__(self,key):
        self._cursor.execute('delete from data_table where key=?',(key,))
    def __setitem__(self,key,value):
        del self[key]
        f = pickle.dumps(value,pickle.HIGHEST_PROTOCOL)
        self._cursor.execute('insert into data_table values(?,?)',(key,sqlite3.Binary(f)))
    def __iter__(self):
        self._cursor.execute('select distinct key from data_table')
        res = list(map(lambda x : x[0],self._cursor.fetchall()))
        return iter(res)


def testing():
    m = SqliteMap("herpus.db")
    for f in m:
        print(f)
        print(m[f])
    print("BEFORE ANYTHING")
    qwer = {'value':1,'qwer':1234}
    asdf = {'value':1232,123:'1324'}
    m[1] = qwer
    m[2] = asdf
    print("TESTITER")
    for f in m:
        print(f)
        print(m[f])
    print("TEST CONTAIN")
    if 1 in m:
        print(m[1])
    print("TESTDELETE")
    del m[2]
    if 2 in m:
        print("SHOULDNT BE HERE")
    else:
        print("GONE AS INTENDED")

if __name__ == "__main__":
    testing()
