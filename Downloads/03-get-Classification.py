#!/usr/bin/env python3
import pymysql
import os
cmd = "rm -r /var/lib/mysql-files/*"
os.system(cmd)
db = pymysql.connect("127.0.0.1", "root", "abc123", "test", charset='utf8' )
cursor = db.cursor()
sql = """select Classification
         into outfile "/var/lib/mysql-files/get-table.txt"
         lines terminated by "\r\n"
         from YAOZHI
         """
cursor.execute(sql)
db.close()
cmd = "cp /var/lib/mysql-files/* /home/student/practice/sql-files"
os.system(cmd)
