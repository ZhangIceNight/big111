# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
 
# num表示记录序号
Url_head = "http://hrb.58.com/"
Url_tail = "/chuzu/pn"
Num = 0
Filename = "/home/student/workspace/58/rent.csv"
 
 
# 把每一页的记录写入文件中
def write_csv(msg_list):
    out = open(Filename, 'a', newline='')
    csv_write = csv.writer(out,dialect='excel')
    for msg in msg_list:
        csv_write.writerow(msg)
    out.close()
 
 
# 访问每一页
def acc_page_msg(page_url):
    web_data = requests.get(page_url).content.decode('utf8')
    soup = BeautifulSoup(web_data, 'html.parser')
    address_list = []
    area_list = []
    num_address = 0
    num_area = 0
    msg_list = []
     
    # 得到了地址列表，以及区域列表
    for tag in soup.find_all(attrs="infor"):
        count = 0
        for a in tag:
            count += 1
            if count == 2:
                address_list.append(a.string)
            elif count == 4:
                if a.string is not None:
                    address_list[num_address] = address_list[num_address] + "-" + a.string
                else:
                    address_list[num_address] = address_list[num_address] + "-Null"
                num_address += 1

#            print(a.string)
#            print("\n")            
    print("success! addr\n")
    # 得到了价格列表
    price_list = []
    for tag in soup.find_all(attrs="money"):
        price_list.append(tag.b.string)
    print("price!!\n")
    # 组合成为一个新的tuple——list并加上序号
    for i in range(len(price_list)):
        txt = (address_list[i], price_list[i])
        msg_list.append(txt)
    print("compose!!\n") 
    # 写入csv
    write_csv(msg_list)
    print("writen!!\n")
 
# 爬所有的页面
def get_pages_urls():
    urls = []
    # 南岗可访问页数70
    for i in range(70):
        urls.append(Url_head + "nangang" + Url_tail + str(i+1))
    # 道里可访问页数70
    for i in range(70):
        urls.append(Url_head + "daoli" + Url_tail + str(i+1))
    # 江北可访问页数70
    for i in range(70):
        urls.append(Url_head + "jiangbei" + Url_tail + str(i+1))
    # 香坊可访问页数70
    for i in range(70):
        urls.append(Url_head + "xiangfang" + Url_tail + str(i+1))
    # 道外可访问页数70
    for i in range(70):
        urls.append(Url_head + "daowai" + Url_tail + str(i+1))
    # 松北可访问页数16
    for i in range(16):
        urls.append(Url_head + "songbei" + Url_tail + str(i+1))
    # 平房可访问页数19
    for i in range(19):
        urls.append(Url_head + "pingfang" + Url_tail + str(i+1))

    return urls
 

if __name__=='__main__':
    print("开始爬虫")
    out = open(Filename, 'a', newline='')
    csv_write = csv.writer(out, dialect='excel')
    title = ("address", "area", "price")
    csv_write.writerow(title)
    out.close()
    url_list = get_pages_urls()
    for url in url_list:
        try:
            acc_page_msg(url)
        except:
            print("格式出错", url)
    print("结束爬虫") 

