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

b = [{"人寿保险":["定期寿险",
              "终生寿险",
              "两全保险"]},
     {"年金保险":["养老年金保险",
              "非养老年金保险"]},
     {"健康保险":["个人税收优惠型健康保险",
                {"非个人税收优惠型健康保险":[{"疾病保险":["重大疾病保险",
                                                     "防癌保险",
                                                     "其它疾病保险"]},
                                         {"医疗保险":["费用补偿型医疗保险",
                                                     "定额给付型医疗保险"]},
                                          "失能收入损失保险",
                                          "护理保险"]}]},
     {"意外伤害保险":""},
     {"委托管理业务":["健康保障委托管理",
                "养老保障委托管理"]}]

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