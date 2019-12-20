#!/usr/bin/env python3
import re
import pymysql
with open ("yaozhi.html", "r", encoding='utf-8') as f:
  str1 = f.read()
pattern1 = re.compile('<td></td>',re.S)
tmp = pattern1.sub("",str1)
pattern2 = re.compile('</td>(\s*)<td>',re.S)
tmp = pattern2.sub("---->",tmp)
pattern3 = re.compile('<td>',re.S)
tmp = pattern3.sub("",tmp)
pattern3 = re.compile('</td>',re.S)
tmp = pattern3.sub("",tmp)
pattern4 = re.compile("---->",re.S)
list1 = pattern4.split(tmp)
n = len(list1)
db = pymysql.connect("127.0.0.1", "root", "abc123", "test", charset='utf8' )
cursor = db.cursor()
sql = """CREATE TABLE YAOZHI (
         Classification    CHAR(30),
         General_Name  CHAR(100),  
         nuclear CHAR(100),
         English_Name CHAR(100),
         Customs_Code  CHAR(100)
         )"""

cursor.execute(sql)
db.close()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------->
db = pymysql.connect("127.0.0.1", "root", "abc123", "test", charset='utf8' )
cursor = db.cursor()
insert_stmt = (
  "INSERT INTO YAOZHI(Classification, General_Name, nuclear, English_Name, Customs_Code)"
  "VALUES (%s, %s, %s, %s, %s)"
)
for i in range(0,n,5): #n is the length of list1

  a1 = list1[i]
  j = i
  i+=1
  a2 = list1[i]
  i+=1
  a3 = list1[i]
  i+=1
  str1 = "蛋白同化制剂"
  str2 = "肽类激素"
  if a1 == str1 or a1 == str2:
    a4 = list1[i]
    i+=1
    a5 = "check"
  else:
    a4 = " "
    a5 = "check"
   # i+=2
   # i+=4    
  data = (a1,a2,a3,a4,a5)
  print (data)
 
  try:
    cursor.execute(insert_stmt,data)
    db.commit()
  except:
    print ("insert error")
    print(i)
    db.rollback()
db.close()                                                                                                                                                                        
#<-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
