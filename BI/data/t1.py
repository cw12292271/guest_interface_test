#!/usr/bin/env.python
# def func(m):
#     m[0] = 20
#     m = [4, 5, 6]
#     return m
#
# l = [1, 2, 3]
# func(l)
# print('l =', l)

# a = 1
# b = 1
# t = {k: v for k,v in locals().items() if not k.startswith("__")}
# c = [a,b]
# print(t)
# for t in t:
#     print(t)
# #dlist=list(t.keys())
# #print(dlist)
#
#
# def shouyi(benjin,huibaolv,nianxian):
#     shouyi = benjin * (1 + huibaolv) ** nianxian
#     print(shouyi)
#
# shouyi(10,0.04,10)
#
# string = "明天就要放假了！\n"
# end = "重要的事情说三遍！\n"
# output_string = string*3 + end
# print(output_string)
#
# price = 300
# hoodie = price
# pants = price
# print("卫衣的原价是"+str(hoodie)+"元。")
# print("运动裤的原价是"+str(pants)+"元。")
# hoodie = hoodie * 0.5
# pants = pants * 0.8
# print("卫衣的\"双11价\"是"+str(hoodie)+"元。")
# print("运动裤的\"双11价\"是"+str(pants)+"元。")
# sum = 0
# for i in range(101):
#     sum = sum + i
# print(sum)
#
# data = {
# 	'肖申克的救赎' : 'Frank Darabont',
# 	'这个杀手不太冷' : 'Luc Besson',
# 	'阿甘正传' : 'Robert Zemeckis'
# }
# for movie in data:
# 	print('电影《' + movie + '》的导演是' + data[movie] + '。')
#
# data = ['章子怡','黄晓明','张震','王力宏']
# for A in data:
#     for B in data:
#         if B is not A:
#             print(A + "和" + B + "是互粉好友。")

# data = [120, 90, 150, 200, 80]
# new_price = []
# for p in data:
#     if p >= 100:
#         new_price.append(p*0.8)
#     else:
#         new_price.append(p * 0.9)
# print(new_price)

# if False:
# 	print("True")
# else:
# 	print("False")

# # 编程判断一个人是否是微博活跃用户
# X = int(input("最近三天登录次数是？"))
# Y = int(input("最近三天发微博数是？"))
# # 判断是否是非常活跃用户
# if X > 20 or Y > 10:
#     print('非常活跃用户')
# # 判断是否是活跃用户
# elif (X >= 10 and X < 20) or (Y >= 5 and Y < 10):
#     print('非常活跃用户')
# # 判断是否是消极用户
# elif X < 3 and Y <= 1:
#     print('消极用户')
# # 判断是否是普通用户
# else:
#     print('普通用户')

# # 编程判断是否含有Trump这个词
# string = "The high-profile engagement between Chinese President Xi Jinping and his U.S. counterpart Donald Trump on Thursday has caught the spotlight globally. Experts said their meeting has borne remarkable fruit, and the forward-looking attitude of the two heads of state towards bilateral cooperation will bring benefits to the two countries, the Asia-Pacific and the world at large."
# if 'Trump' in string:
#     print("This article maybe about Trump.")
# else:
#     print("This article maybe not about Trump.")
#
# #编程判断某演员是否出演了某电影
# data = {
#   '芳华' : ['黄轩','苗苗'],
#   '战狼2' : ['吴京','吴刚','卢婧姗'],
#   '无问西东' : ['章子怡','黄晓明','张震','王力宏'],
#   '大兵小将' : ['成龙', '王力宏', '刘承俊']
# }
# name = input("请输入要查询的演员名：")
# d = ""
# for movie in data:
#     for actors in data[movie]:
#         if name in actors:
#             d = '《' + str(movie) + '》'
# d = d + d
# if d != "":
#     print(name + '出演了电影' + d )
# else:
#     print(name + '未出演电影' )
# # 编程判断年终考勤是否合格
# data = [21, 22, 22, 20, 23, 19, 20, 21, 23, 20, 22, 20]
# # 建立一个空列表
# not_good = []
# # 当有考勤不合格的数据时，添加到列表里
# for one in data:
#     if one <  20:
#         not_good.append(one)
# # 如果列表里有数据，则判定考勤不合格
# if not_good:
#     print('考勤不合格')
# else:
#     print('考勤合格')
# # 定义一个能判断重量的函数
# def order(weight):
#     if weight >= 3:
#         total_prices = weight * 5
#     else:
#         total_prices = weight * 6
#     return total_prices
# # 重量数据来源于input输入
# weight = int(input('需要购买的橘子的重量：'))
# total_prices = order(weight)
# # 打印结果
# print('总价' + '：' + str(total_prices))
# 考勤数据
# list = [22, 23, 20, 19, 21, 22, 22, 23, 24, 20, 20, 22]
# # 定义一个函数统计不合格考勤次数
# def check_in():
#     count = 0
#     for i in list:
#         if i < 20:
#             count = count + 1
#     if count != 0:
#         print(str(count) + '个月考勤不合格')
#     else:
#         print('本月全勤')
# check_in()
# # 引入random库
# import random
# # 调用randint函数
# r = random.randint(1,6)
# # 打印结果
# print(r)
# # 最佳影片提名名单
# list = ['fff','泰坦尼克号', '洛城机密', '骄阳似我', '一脱到底', '尽善尽美']
# # 定义一个能添加*的函数
# def best_movie():
#     i = 0
#     for movie in list:
#         if movie == '泰坦尼克号':
#             movie = '*' + movie
#             list[i] = movie
#         i = i+1
#     print(list)
# # 打印结果
# best_movie()
# # 分割字符串
# string = "哈利、罗恩、赫敏"
# list = string.split('、')
# print(list)
# # 列表数据
# list = [1,2,3,4,5,6,7,8,9]
# # 实现列表中的元素都加100
# i = 0
# for a in list:
#     a = a + 100
#     list[i] = a
#     i = i+1
# # 打印列表的第3-6个元素、和倒数第一个元素
# print("列表的第3-6个元素是"+str(list[2:6]))
# print("列表的倒数第一个元素是"+str(list[-1]))

# # 电影及演员数据
# data = {
# 	'霸王别姬' : ['张国荣','张丰毅','巩俐','葛优'],
# 	'无间道' : ['刘德华','梁朝伟','黄秋生','曾志伟','郑秀文'],
# 	'活着' : ['葛优','巩俐','姜武','牛犇','郭涛']
# }
# # 遍历字典中的元素
# for key in data:
#     value = data[key]
# # 将列表转换为字符串
#     v = '、'.join(value)
#     print("电影《"+ key + "》的主演有"+ v + "。")

# # 姓名名单数据
# string = "哈利·波特、罗恩·韦斯莱、赫敏·格兰杰、乔治·韦斯莱、弗雷·韦斯莱、纳威、卢娜、阿不思·珀西瓦尔·邓布立多"
#
# # 筛选出姓氏并打印出来
# name = string.split('、')
# result =  []
# for new_name in name:
#     if len(new_name.split('·')) >= 2:
#         lastname = new_name.split('·')[-1]
#         if lastname not in result:
#             result.append(lastname)
# print('、'.join(result))

# 姓名名单数据
string = "哈利·波特、罗恩·韦斯莱、赫敏·格兰杰、乔治·韦斯莱、弗雷·韦斯莱、纳威、卢娜、阿不思·珀西瓦尔·邓布立多"
last_name_set = set([])
# 分割字符串为列表
data = string.split("、")
for name in data:
	# 利用·字符来分割名字
    list = name.split("·")
    # 判断名字中是否有多个分割
    if len(list) >= 2:
        last_name = list[-1]
        # 在集合中添加元素
        last_name_set.add(last_name)
# 打印结果
print(last_name_set)