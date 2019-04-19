
'''
[{"人寿保险":["定期寿险","终生寿险","两全保险"]},
 {"年金保险":["养老年金保险","非养老年金保险"]},
 {"健康保险":["个人税收优惠型健康保险",{"非个人税收优惠型健康保险":[{"疾病保险":["重大疾病保险","防癌保险","其它疾病保险"]},{"医疗保险":["费用补偿型医疗保险","定额给付型医疗保险"]},"失能收入损失保险","护理保险"]}]},
"意外伤害保险",
 {"委托管理业务":["健康保障委托管理","养老保障委托管理"]}]
'''

import time
import requests

import re
import xlwt


def getc5(c1,c2,c3,c4):
    if c2 == "":
        c5 = c1
    elif c3 == "":
        c5 = c2
    elif c4 == "":
        c5 = c3
    else:
        c5 = c4
    return c5


def getProductId(c1,c2,c3,c4):
    global list_row
    title_row = [["一级", "二级", "三级", "四级", 'pdf编号','公司名称', '产品名称', '产品类别', '设计类型', '产品特殊属性', '承保方式', '保险期间类型', '产品交费方式', '产品条款文字编码', '产品销售状态','停止销售日期']]
    list_row = []
    c5 = getc5(c1,c2,c3,c4)
    payload = { 'pageNo': 1,
                'prodTypeCodeOne': c1,
                'prodTypeCodeTwo': c2,
                'prodTypeCodeThree': c3,
                'prodTypeCodeFour': c4,
                'prodTermsShow.prodTypeCode': c5,
                'pageSize': 3000
                }

    r = requests.post(url, headers=headers,data = payload)
    idlist = re.findall( r"detailed\('(.*)','detailed", r.text)
    for id in idlist:
        req = requests.get(url2 + id + '.html')
        if req.encoding == 'ISO-8859-1':
            encodings = requests.utils.get_encodings_from_content(req.text)
            if encodings:
                encoding = encodings[0]
            else:
                encoding = req.apparent_encoding

            # encode_content = req.content.decode(encoding, 'replace').encode('utf-8', 'replace')
            global encode_content
            encode_content = req.content.decode(encoding, 'replace')  # 如果设置为replace，则会用?取代非法字符；

        original_list = [c1, c2, c3, c4]
        for i in range(4):
            if original_list[i] != "":
                original_list[i] = dt[original_list[i]]
            else:
                pass
        original_list.extend([id])
        original_list.extend(re.findall(r'align="left" >(.*)&nbsp;', encode_content))
        original_list.extend(re.findall(r'align="left">(.*)&nbsp;', encode_content))
        global num
        num = num + 1
        print(num ,original_list)
        list_row.append(original_list)

        # r = requests.get(url3 + id + '_TERMS.PDF')
        # with open('./pdf_data/{}.pdf'.format(id), 'wb') as fd:
        #     for chunk in r.iter_content(500):
        #         fd.write(chunk)
    title_row.extend(list_row)
    list_row=title_row

    #写数据进Excel
    #workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet('{}'.format(dt[c5]))
    for i in range(len(list_row)):
        for j in range(len(list_row[i])):
            worksheet.write(i, j, list_row[i][j])
    workbook.save('人身险产品信息库.xls')



if __name__ == '__main__':
    url = 'http://tiaokuan.iachina.cn:8090/sinopipi/loginServlet/publicQueryResult.do'
    url2 = 'http://www.iachina.cn/IC/tkk/02/'
    url3 = 'http://www.iachina.cn/IC/tkk/03/'
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
    dt = {"ProdTypeCode_00": "人寿保险", "ProdTypeCode_00_00": "定期寿险", "ProdTypeCode_00_01": "终生寿险",
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
    a = {"ProdTypeCode_00": {"ProdTypeCode_00_00": "",
                             "ProdTypeCode_00_01": "",
                             "ProdTypeCode_00_02": ""},
         "ProdTypeCode_01": {"ProdTypeCode_01_00": "",
                             "ProdTypeCode_01_01": ""},
         "ProdTypeCode_02": {"ProdTypeCode_02_00": "",
                             "ProdTypeCode_02_01": {"ProdTypeCode_02_01_00": {"ProdTypeCode_02_01_00_00": "",
                                                                              "ProdTypeCode_02_01_00_01": "",
                                                                              "ProdTypeCode_02_01_00_02": ""},
                                                    "ProdTypeCode_02_01_01": {"ProdTypeCode_02_01_01_00": "",
                                                                              "ProdTypeCode_02_01_01_01": ""},
                                                    "ProdTypeCode_02_01_02": "",
                                                    "ProdTypeCode_02_01_03": ""}},
         "ProdTypeCode_03": '',
         "ProdTypeCode_04": {"ProdTypeCode_04_00": "",
                             "ProdTypeCode_04_01": ""}
         }

    num = 0
    print('\n','{0:*^20}'.format('开始'), '\n')
    workbook = xlwt.Workbook(encoding='ascii')
    for c1, v1 in a.items():
        c2, c3, c4 = "", "", ""
        if type(v1) == dict:
            for c2, v2 in v1.items():
                if type(v2) == dict:
                    for c3, v3 in v2.items():
                        if type(v3) == dict:
                            for c4, v4 in v3.items():
                                getProductId(c1, c2, c3, c4)
                        else:
                            getProductId(c1, c2, c3, v3)
                else:
                    getProductId(c1, c2, v2, c4)
        else:
            getProductId(c1, v1, c3, c4)

    workbook.save('人身险产品信息库.xls')

    print('\n','{0:*^20}'.format('结束'), '\n')