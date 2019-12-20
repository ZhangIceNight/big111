#!/usr/bin/env python3
import os
def main():
  cmd = "hadoop fs -get /root/experiment/output/part-r-00000  /home/student/practice"
  os.system(cmd)
if __name__ == "__main__":
  main() 

