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
  base_url = "https://db.yaozh.com/xfjml?p="
  header = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0",
  }
  rets = [] 
  for i in range(4):
    j = i+1
    url = base_url + str(j) + """&pageSize=30"""
    resp = requests.get(url, headers=header)
    data = resp.content.decode("utf-8")
  
    pattern = re.compile("""<td>.*</td>""")
    ret = pattern.findall(data)
    rets.append(ret)
#  print(rets)
  with open("yaozhi.html", "w") as f:
    for i in rets:
      f.write(" ".join(i))
      f.write("\n")






if __name__ == "__main__":
  main()
