import re

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import time
import requests

import xlwt


options = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'D:\PycharmProjects\webot2.0\spider\data_pdf'}
options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(executable_path='C:\ProgramData\Anaconda3\chromedriver.exe', chrome_options=options)

driver.implicitly_wait(10)
#driver.maximize_window()
base_url = 'http://www.iachina.cn/art/2017/6/29/art_71_45682.html'
driver.get(base_url)
time.sleep(1)

first_windows = driver.current_window_handle

frames1 = driver.find_element_by_xpath("/html/body/div[3]/ul/li[1]/div[3]/div[1]/div/p/iframe")
#切换到frame1
driver.switch_to_frame(frames1)


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
    pagecount = int(序号[-1])
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
    time.sleep(1)
    list_row = [["","","","",'公司名称', '产品名称', '产品类别', '设计类型', '产品特殊属性', '承保方式', '保险期间类型', '产品交费方式','产品条款文字编码', '产品销售状态', '停止销售日期']]

    n = 0
    #total_pages = 1
    for k in range(total_pages//10 + 1):
        if total_pages < 10 or k == total_pages//10:
            detailscount = total_pages%10
        else:
            detailscount = 10
        for j in range(detailscount):
            dict = {"ProdTypeCode_00": "人寿保险", "ProdTypeCode_00_00": "定期寿险", "ProdTypeCode_00_01": "终生寿险",
                    "ProdTypeCode_00_02": "两全保险",
                    "ProdTypeCode_01": "年金保险", "ProdTypeCode_01_00": "养老年金保险", "ProdTypeCode_01_01": "非养老年金保险",
                    "ProdTypeCode_02": "健康保险", "ProdTypeCode_02_00": "个人税收优惠型健康保险",
                    "ProdTypeCode_02_01": "非个人税收优惠型健康保险",
                    "ProdTypeCode_02_01_00": "疾病保险",
                    "ProdTypeCode_02_01_00_00": "重大疾病保险",
                    "ProdTypeCode_02_01_00_01": "防癌保险",
                    "ProdTypeCode_02_01_00_02": "其它疾病保险",
                    "ProdTypeCode_02_01_01": "医疗保险",
                    "ProdTypeCode_02_01_01_00": "费用补偿型医疗保险",
                    "ProdTypeCode_02_01_01_01": "定额给付型医疗保险",
                    "ProdTypeCode_02_01_02": "失能收入损失保险",
                    "ProdTypeCode_02_01_03": "护理保险",
                    "ProdTypeCode_03": "意外伤害保险",
                    "ProdTypeCode_04": "委托管理业务", "ProdTypeCode_04_00": "健康保障委托管理", "ProdTypeCode_04_01": "养老保障委托管理"}
            original_list = [c1, c2, c3, c4]
            for i in range(4):
                if original_list[i] == "":
                    original_list[i] = ""
                else:
                    original_list[i] = dict[original_list[i]]
            driver.find_element_by_id("detailed{}".format(j + 1)).click()
            time.sleep(1)
            all_handles = driver.window_handles

            for handle in all_handles:
                if handle != first_windows:
                    driver.switch_to_window(handle)

                    driver.find_element_by_link_text("查看产品条款基本信息").click()
                    time.sleep(1)
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

                    original_list.extend(re.findall(r'align="left" >(.*)&nbsp;', encode_content))
                    original_list.extend(re.findall(r'align="left">(.*)&nbsp;', encode_content))
                    n = n+1
                    print(n,original_list)
                    list_row.append(original_list)

                    #返回下载pdf页面
                    driver.back()
                    frames2 = driver.find_element_by_xpath('//*[@id="tr2"]/td/iframe')
                    # 切换到pdf文件frame2
                    driver.switch_to_frame(frames2)
                    driver.find_element_by_id("download").click()
                    time.sleep(3)


                    driver.close()
                    driver.switch_to_window(all_handles[0])
                    driver.switch_to_frame(frames1)
                    time.sleep(1)


        #翻页
        if k < total_pages//10:
            driver.find_element_by_xpath("/html/body/form[1]/table[4]/tbody/tr/td[4]/a/img").click()
            time.sleep(1)
        else:
            pass

    # 写数据进Excel
    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet('My Worksheet')
    for i in range(len(list_row)):
        for j in range(len(list_row[i])):
            worksheet.write(i, j, list_row[i][j])
    workbook.save('Excel_Workbook.xls')





#a = [{"ProdTypeCode_00":["ProdTypeCode_00_00",
#                          "ProdTypeCode_00_01",
#                          "ProdTypeCode_00_02"]},
#      {"ProdTypeCode_01":["ProdTypeCode_01_00",
#                          "ProdTypeCode_01_01"]},
#      {"ProdTypeCode_02":["ProdTypeCode_02_00",
#                 {"ProdTypeCode_02_01":[{"ProdTypeCode_02_01_00":
#                                          ["ProdTypeCode_02_01_00_00",
#                                           "ProdTypeCode_02_01_00_01",
#                                           "ProdTypeCode_02_01_00_02"]
#                                             },
#                                      {"ProdTypeCode_02_01_01":
#                                         ["ProdTypeCode_02_01_01_00",
#                                         "ProdTypeCode_02_01_01_01"]
#                                             },
#                                           "ProdTypeCode_02_01_02",
#                                           "ProdTypeCode_02_01_03"]
#                 }
#               ]},
#      {"ProdTypeCode_03":""},
#      {"ProdTypeCode_04":["ProdTypeCode_04_00",
#                          "ProdTypeCode_04_01"]}]

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
              ]
      },
     {"ProdTypeCode_03":""},
     {"ProdTypeCode_04":["ProdTypeCode_04_00","ProdTypeCode_04_01"]}]

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
                                        spider(c1, c2, c3, c4)
                            else:
                                spider(c1, c2, c3, c4)

                else:
                    c2 = j
                    spider(c1, c2, c3, c4)
        else:
            spider(c1, c2, c3, c4)
    print('{0:*^20}'.format('结束'),'\n')

driver.quit()