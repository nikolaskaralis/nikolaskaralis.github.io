#!/usr/bin/python
licence = '''
#    Copyright (C) 2012, 2013 Nikolas Karalis
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    http://www.nikolaskaralis.gr
#    email : nikolaskaralis@gmail.com
'''
print licence

import sqlite3, random, os, shutil, unicodedata
from os.path import expanduser

home_path = expanduser("~")
# Set Papers2 path
input_path = home_path+'/Library/Application Support/Papers2/'
# Set output path
output_path = home_path+'/Desktop/Collections/'
try:
  os.makedirs(output_path);
except:
  output_path += `random.randint(1000, 9999)`+'/'
  os.makedirs(output_path);
  
conn = sqlite3.connect(input_path+'Library.papers2/Database.papersdb');
c = conn.cursor();
c.execute('select distinct collection from CollectionItem;');
temp = c.fetchall();
collection = [i[0] for i in temp]
errors = []

for col in collection:
  # Get category title
  c.execute('select * from Collection where rowid='+`col`);
  temp = c.fetchall()[0];
  title=temp[7]

  # Get paper rowids from the CollectionItem table
  c.execute('select * from CollectionItem where collection='+`col`);
  temp = c.fetchall();
  paper_rowid = [i[4] for i in temp]
  
  # Create collection subfolders
  try:
    collecion_path=output_path+title;
    os.makedirs(collecion_path)
  except:
    collecion_path=output_path+title+`random.randint(1000, 9999)`;
    os.makedirs(collecion_path)
  
  print title + ' : ' + `len(paper_rowid)` + ' papers.'
    
  # Get pdf paths from the PDF table
  paths=[]
  for id in paper_rowid:
    c.execute('select * from PDF where object_id='+`id`);
    temp = c.fetchall()[0];
    paths.append(temp[14]);
    full_paths = [unicodedata.normalize('NFKD', input_path+i).encode('ascii','ignore') for i in paths]
    
  # Copy pdf files to the ouput directory  

  for i in full_paths:
    try:
      shutil.copy2(i, collecion_path)  
    except:
      errors.append(i)

print '\nErrors:'
for i in errors:
  print i

  
conn.close()