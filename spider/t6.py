c1,c2,c3,c4 = "","","",""
# a = [{"ProdTypeCode_00": [{"ProdTypeCode_00_00":""},
#                           {"ProdTypeCode_00_01":""},
#                           {"ProdTypeCode_00_02":""}]
#       },
#      {"ProdTypeCode_01": [{"ProdTypeCode_01_00":""},
#                           {"ProdTypeCode_01_01":""}]
#       },
#      {"ProdTypeCode_02": [{"ProdTypeCode_02_00" :""},
#                           {"ProdTypeCode_02_01": [{"ProdTypeCode_02_01_00" :["ProdTypeCode_02_01_00_00",
#                                                                             "ProdTypeCode_02_01_00_01",
#                                                                             "ProdTypeCode_02_01_00_02"]},
#                                                   {"ProdTypeCode_02_01_01" :["ProdTypeCode_02_01_01_00",
#                                                                             "ProdTypeCode_02_01_01_01"]},
#                                                   {"ProdTypeCode_02_01_02" :""},
#                                                   {"ProdTypeCode_02_01_03" :""}]}]
#       },
#      {"ProdTypeCode_03": ''},
#      {"ProdTypeCode_04": [{"ProdTypeCode_04_00":""},
#                           {"ProdTypeCode_04_01":""}]
#       }]

# n1,n2 = 1,1
# for j1 in a:
#     for k1,v1 in j1.items():
#         c1 = k1
#         if v1 != '':
#             for j2 in v1:
#                 for k2, v2 in j2.items():
#                     c2 = k2
#                     if v2 != '':
#                         for j3 in v2:
#                             for k3, v3 in j3.items():
#                                 c3 = k3
#                                 if v3 != '':
#                                     for j4 in v3:
#                                         for k4, v4 in j2.items():
#                                             c4 = k4
#                                             print('{}'.format(n1), c1, c2, c3, c4)
#                                             n1 = n1 + 1
#                                 else:
#                                     print('{}'.format(n1), c1, c2, c3, c4)
#                                     n1 = n1 + 1
#                     else:
#                         print('{}'.format(n1), c1, c2, c3, c4)
#                         n1 = n1 + 1
#         else:
#             print('{}'.format(n1), c1, c2, c3, c4)
#             n1 = n1 + 1

a = {"ProdTypeCode_00": {"ProdTypeCode_00_00":"",
                          "ProdTypeCode_00_01":"",
                          "ProdTypeCode_00_02":""},
     "ProdTypeCode_01": {"ProdTypeCode_01_00":"",
                          "ProdTypeCode_01_01":""},
     "ProdTypeCode_02": {"ProdTypeCode_02_00" :"",
                         "ProdTypeCode_02_01": {"ProdTypeCode_02_01_00" :{"ProdTypeCode_02_01_00_00":"",
                                                                            "ProdTypeCode_02_01_00_01":"",
                                                                            "ProdTypeCode_02_01_00_02":""},
                                                  "ProdTypeCode_02_01_01" :{"ProdTypeCode_02_01_01_00":"",
                                                                            "ProdTypeCode_02_01_01_01":""},
                                                  "ProdTypeCode_02_01_02" :"",
                                                  "ProdTypeCode_02_01_03" :""}},
     "ProdTypeCode_03": '',
     "ProdTypeCode_04": {"ProdTypeCode_04_00":"",
                          "ProdTypeCode_04_01":""}
      }

for c1, v1 in a.items():
    c2, c3, c4 = "", "", ""
    if type(v1) == dict:
        for c2, v2 in v1.items():
            if type(v2) == dict:
                for c3, v3 in v2.items():
                    if type(v3) == dict:
                        for c4, v4 in v3.items():
                            print(c1, c2, c3, c4, '\n')
                    else:
                        print(c1, c2, c3, v3, '\n')
            else:
                print(c1, c2, v2, c4, '\n')
    else:
        print(c1, v1, c3, c4, '\n')

