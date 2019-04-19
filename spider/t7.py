#coding: utf-8
import xlwt
from xlwt import Workbook


wb = Workbook()
ws = wb.add_sheet('Product')
ws_1 = wb.add_sheet('Other')

fontSize = xlwt.easyxf('font:height 200, name Calibri; align: horiz center;')   #字体自定义

row0 = [u'名目',u'链接',u'备注']
row1 = [u'name',u'file',u'url']

def title_write(row,ws):
    #生成标题
    for i in range(0,len(row)):
        col = ws.col(i)
        col.width=256*18
        if i == (len(row)-1):
            ws.col(i).width = 256*23
            ws.write(0,i,row[i],xlwt.easyxf('font:height 200, name Arial_Unicode_MS, colour_index black, bold on;align: horiz center;'))
title_write(row0,ws)
title_write(row1,ws_1)
data = [{'1':[u'福尔摩斯探案集',u'http://www.fuermositanan.com/',u'推理'],'2':[u'The Sherlock Holmes stories',u'Arthur Conan Doyle',u'https://ebooks.adelaide.edu.au/d/doyle/arthur_conan/']}]#这里演示写死了，根据实际需求更改

x = 1
for i in data:
    rows_0 = i['1']
    rows_1 = i['2']
    def rows_write(content,ws):
        #生成内容
        for num,rows in enumerate(content):
           rows if rows != None else ''
           ws.write(x, num, rows, fontSize)
    rows_write(rows_0,ws)
    rows_write(rows_1,ws_1)
    x += 1

fname='Books.xls'
wb.save(fname)