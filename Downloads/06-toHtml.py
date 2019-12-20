#!/usr/bin/env python3
import requests 
import re
import sys
import io 
def setup_io(): 
  sys.stdout = sys.__stdout__ = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', line_buffering=True) 
  sys.stderr = sys.__stderr__ = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8', line_buffering=True) 
setup_io()

def main():
  with open("/home/student/practice/part-r-00000", "r") as f:
    str1 = f.read()  
  ret = str1.split("\n")
  html = """<html>
<head></head>
<body>
<ul>
"""
  for i in ret:
    html += """<li><a>"""
    #html += i[0]
    #html += """">""" 
    html += i
    html += """</a></li>""" 
  html += """</ul></body></html>""" 


  with open("/home/student/practice/news-YAOZHI.html", "w", encoding = "utf-8") as f:
    f.write(html)
if __name__ == "__main__":
  main()

