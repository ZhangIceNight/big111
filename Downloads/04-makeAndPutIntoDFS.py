#!/usr/bin/env python3
import os
def main():
  cmd = "hadoop fs -rm -r /root"
  os.system(cmd)
  cmd = "hadoop fs -mkdir -p /root/experiment/datas"
  os.system(cmd)
  cmd = "hadoop fs -put /home/student/practice/sql-files/get-table.txt  /root/experiment/datas"
  os.system(cmd)
if __name__ == "__main__":
  main() 
