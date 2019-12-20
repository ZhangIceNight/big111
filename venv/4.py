# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
from fontTools.ttLib import TTFont, BytesIO
import base64
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
#
def make_font_file(base64_string):
    bin_data = base64.decodebytes(base64_string.encode())
    with open('text.otf','wb') as f:
        f.write(bin_data)
    return bin_data
#
def convert_font_to_xml(bin_data):
    # 由于TTFont接收一个文件类型
    # BytesIO(bin_data) 把二进制数据当作文件来操作
    font = TTFont(BytesIO(bin_data))
    font.saveXML("text.xml")









#
def get_num(response, string):
    base64_str = response.text.split("base64,")[1].split("'")[0].strip()
    bin_data = make_font_file(base64_str)
    convert_font_to_xml(bin_data)
    # 获取对应关系
    font = TTFont(BytesIO(make_font_file(base64_str)))
    uniList = font['cmap'].tables[0].ttFont.getGlyphOrder()
    c = font['cmap'].tables[0].ttFont.tables['cmap'].tables[0].cmap
    # c = font.getBestCmap()
    print('cmap is:::::', c)

    ret_list = []

    for char in string:
        decode_num = ord(char)
        num = c[decode_num]
        num = int(num[-2:])-1
        ret_list.append(num)

    return ret_list

# get the secret_num
#def get_secret_num(mistake_word):



# 访问每一页
def acc_page_msg(page_url):
    response = requests.get(page_url)
    web_data = response.content.decode('utf8')
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
                #print(a.string)
            elif count == 4:
                if a.string is not None:
                    address_list[num_address] = address_list[num_address] + "-" + a.string
                else:
                    address_list[num_address] = address_list[num_address] + "-Null"
                num_address += 1

#            print(a.string)
#            print("\n")
    print("num_address:")
    print(num_address)
    print("\n")
    #print("success! addr\n")
    # 得到了区域列表
    for tag in soup.find_all(attrs="nav-top-bar"):
        count = 0
        for c in tag:
            count += 1
            if count == 8:
                ans=c.string[0:2]
    for i in range(len(address_list)):
        area_list.append(ans)
        #print("    ")
        #print(ans)
        num_area += 1
    # 得到了价格列表
    price_list = []
    for tag in soup.find_all(attrs="money"):
        count = 0
        for b in tag:
            count += 1
            if count == 2:
                price_list.append("".join('%s' %id for id in get_num(response,b.string)))
                #print("     ")
                #print("".join('%s' %id for id in get_num(b.string)))
                #print("")
    #print("price!!\n")
    # 组合成为一个新的tuple——list并加上序号
    for i in range(len(area_list)):
        txt = (address_list[i], area_list[i], price_list[i])
        msg_list.append(txt)
        print(txt)
    #print("compose!!\n")
    # 写入csv
    write_csv(msg_list)
    #print("writen!!\n")

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
     #松北可访问页数16
    for i in range(16):
       urls.append(Url_head + "sbheb" + Url_tail + str(i+1))
    #平房可访问页数19
    for i in range(19):
        urls.append(Url_head + "pingfang" + Url_tail + str(i + 1))

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
            print(url)
            print("\n")
        except:
            print("格式出错", url)
    print("结束爬虫")
