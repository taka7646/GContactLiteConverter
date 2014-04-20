# -*- coding: utf-8 -*-
from PList import PList
import os
import re
import csv
import codecs

path = '../data/'

re_file = re.compile('\d+\.plist')
files = filter(lambda n: re_file.match(n), os.listdir('../data/'))

users = {}
for f in files:
  plist = PList.fromfile( path + f )
  id = plist['ID']
  plist.setdefault('Phone', [{'Value':''}])
  plist.setdefault('Email', [{'Value':''}])
  plist.setdefault('LastName', '')
  plist['groups'] = []
  users[id] = plist



list = PList.fromfile( path + 'group.plist')
groups = {}
for g in list:
  if g.has_key("Member"):
    id = g["ID"]
    groups[id] = g
    for m in g["Member"]:
      if not users[m].has_key( 'groups' ):
        users[m]['groups'] = []
      users[m]['groups'].append(id)


#print users[1]
#print users
filename = "./list.csv"
f = file(filename, 'w')
#f = codecs.lookup('utf_8')[-1](f)
writecsv = csv.writer(f, lineterminator='\n')
row = [u'id',u'名前',u'名前2',u'電話番号',u'e-mail',u'グループ']
writecsv.writerow(map(lambda s: s.encode('cp932'), row))
for id,u in users.items():
  row = [str(id),u['Title'], u['LastName'], str(u['Phone'][0]['Value']), u['Email'][0]['Value'] ]
  row.extend([ groups[id]['GroupName'] for id in u['groups'] ])
  writecsv.writerow(map(lambda s: s.encode('cp932'), row))
#  print ",".join(row)
