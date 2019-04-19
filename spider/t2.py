import re

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import time
import requests

import xlwt


list_row =[ ['公司名称','产品名称','产品类别','设计类型','产品特殊属性','承保方式','保险期间类型','产品交费方式','产品条款文字编码','产品销售状态','停止销售日期']]

driver = webdriver.Chrome()

driver.implicitly_wait(10)
#driver.maximize_window()
base_url = 'http://www.iachina.cn/art/2017/6/29/art_71_45682.html'
driver.get(base_url)
time.sleep(1)

print('--1--',driver.window_handles)
first_windows = driver.current_window_handle

frames1 = driver.find_element_by_xpath("/html/body/div[3]/ul/li[1]/div[3]/div[1]/div/p/iframe")
#切换到frame1
driver.switch_to_frame(frames1)

import re

import requests
from selenium import webdriver

apis = 'http://tiaokuan.iachina.cn:8090/sinopipi/loginServlet/publicQueryResult.do'

def pagecount(c1,c2,c3,c4,c5):
    headers = {'Connection':'keep-alive',
                'Content-Length':'454',
                'Cache-Control': 'max-age=0',
                'Origin': 'http://tiaokuan.iachina.cn:8090',
                'Upgrade-Insecure-Requests': '1',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Referer': 'http://tiaokuan.iachina.cn:8090/sinopipi/loginServlet/publicQueryResult.do',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
                'Cookie': 'JSESSIONID=3F04E3108EADC7377AD6B88D7C1B7767'
    }

    data = {'pageNo': 1,
            'pageCount': '',
            'prodTermsShow.prodName': '',
            'prodTermsShow.insComName': '',
            'prodTermsShow.insItemCode': '',
            'prodTermsShow.saleStatus': '',
            'prodTermsShow.specialAttri': '',
            'prodTermsShow.insType': '',
            'prodTermsShow.insPerdType': '',
            'prodTypeCodeOne': c1,
            'prodTypeCodeTwo': c2,
            'prodTypeCodeThree': c3,
            'prodTypeCodeFour': c4,
            'prodTermsShow.prodTypeCode': c5,
            'prodTermsShow.prodDesiCode': '',
            'pageSize': 3000
            }

    r = requests.post(apis, headers=headers,data = data)
    序号 = re.findall( r'"width:3%" >(.*)</td>', r.text)
    pagecount = int(序号[-1])//10
    return pagecount

def spider(c1,c2,c3,c4):
    if c1 != "":
        Select(driver.find_element_by_id("prodTypeCode1")).select_by_value(c1)
        c5 = c1
        if c2 != "":
            Select(driver.find_element_by_id("prodTypeCode2")).select_by_value(c2)
            c5 = c2
            if c3 != "":
                Select(driver.find_element_by_id("prodTypeCode3")).select_by_value(c3)
                c5 = c3
                if c4 != "":
                    Select(driver.find_element_by_id("prodTypeCode4")).select_by_value(c4)
                    c5 = c4

    total_pages = pagecount(c1,c2,c3,c4,c5)
    driver.find_element_by_id("but1").click()
    for i in range(10):
        driver.find_element_by_id("detailed{}".format(i + 1)).click()

        print('--2--',driver.window_handles)
        all_handles = driver.window_handles

        for handle in all_handles:
            if handle != first_windows:
                driver.switch_to_window(handle)
                driver.find_element_by_link_text("查看产品条款基本信息").click()
                req = requests.get(driver.current_url)

                if req.encoding == 'ISO-8859-1':
                    encodings = requests.utils.get_encodings_from_content(req.text)
                    if encodings:
                        encoding = encodings[0]
                    else:
                        encoding = req.apparent_encoding

                    # encode_content = req.content.decode(encoding, 'replace').encode('utf-8', 'replace')
                    global encode_content
                    encode_content = req.content.decode(encoding, 'replace')  # 如果设置为replace，则会用?取代非法字符；

                #print(type(encode_content))
                产品条款基本信息 = re.findall( r'align="left" >(.*)&nbsp;', encode_content)
                产品条款基本信息.extend(re.findall( r'align="left">(.*)&nbsp;', encode_content))
                list_row.append(产品条款基本信息)
                driver.close()
                print('--3--',all_handles[0])
                driver.switch_to_window(all_handles[0])
                driver.switch_to_frame(frames1)

    time.sleep(3)
    #写数据进Excel


    workbook = xlwt.Workbook(encoding = 'ascii')
    worksheet = workbook.add_sheet('My Worksheet')
    print(list_row)
    for i in range(len(list_row)):
        for j in range(len(list_row[i])):
            worksheet.write(i, j, list_row[i][j])


    workbook.save('Excel_Workbook.xls')


a = [{"ProdTypeCode_00":["ProdTypeCode_00_00",
                         "ProdTypeCode_00_01",
                         "ProdTypeCode_00_02"]},
     {"ProdTypeCode_01":["ProdTypeCode_01_00",
                         "ProdTypeCode_01_01"]},
     {"ProdTypeCode_02":["ProdTypeCode_02_00",
                {"ProdTypeCode_02_01":[{"ProdTypeCode_02_01_00":
                                         ["ProdTypeCode_02_01_00_00",
                                          "ProdTypeCode_02_01_00_01",
                                          "ProdTypeCode_02_01_00_02"]
                                            },
                                     {"ProdTypeCode_02_01_01":
                                        ["ProdTypeCode_02_01_01_00",
                                        "ProdTypeCode_02_01_01_01"]
                                            },
                                          "ProdTypeCode_02_01_02",
                                          "ProdTypeCode_02_01_03"]
                }
              ]},
     {"ProdTypeCode_03":""},
     {"ProdTypeCode_04":["ProdTypeCode_04_00",
                         "ProdTypeCode_04_01"]}]
sum = 0
for i in a:
    c1,c2,c3,c4 = '','','',''
    print('{0:*^20}'.format('开始'), '\n')
    for k1,v1 in i.items():
        c1 = k1
        if v1 != "":
            for j in v1:
                if type(j) == dict:
                    for k2, v2 in j.items():
                        c2 = k2
                        for s in v2:
                            if type(s) == dict:
                                for k3, v3 in s.items():
                                    c3 = k3
                                    for c4 in v3:
                                        print(c1,'\n',c2,'\n',c3,'\n',c4,'\n')
                                        print("执行")
                                        sum = sum +1
                            else:
                                print(c1,'\n',c2,'\n',c3,'\n',c4,'\n')
                                print("执行")
                                sum = sum + 1

                else:
                    c2 = j
                    print(c1,'\n',c2,'\n',c3,'\n',c4,'\n')
                    print("执行")
                    sum = sum + 1
        else:
            print(c1,'\n',c2,'\n',c3,'\n',c4,'\n')
            print("执行")
            sum = sum + 1
    print('{0:*^20}'.format('结束'),'\n')
print('/////',sum)
