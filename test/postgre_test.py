import psycopg2
import json
import leagreq.match_detail as match_detail
conn = psycopg2.connect(host='localhost',database='FriendLeague',user='thomas',password='2012*GbS')
cursor = conn.cursor()
name = '333asd'
#cursor.execute('select account_id from analytics_account where name = %s',[name])
a = [12345,23456]
#cursor.execute('update analytics_account set solo_match_list=array_cat(solo_match_list,%s::bigint[]) where account_id=44649467',[a])
#cursor.execute('update analytics_account set solo_match_list=array[]::bigint[] where account_id=44649467',[a])
m = {'derp':'x',1:'hee'}
ms = json.dumps(m)
#cursor.execute('insert into analytics_match_detail values(%s,%s)',[1,ms])
cursor.execute('select match_data from analytics_match_detail where match_id=1')
s = cursor.fetchone()
s = s[0]
print(s)
print(s['1'])
cursor.execute('select account_id from analytics_account where account_id=1')
r = cursor.fetchone()
r = r[0]
cursor.close()
conn.commit()
conn.close()
