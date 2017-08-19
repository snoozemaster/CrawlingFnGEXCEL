from urllib.request import urlopen
from bs4 import BeautifulSoup
import sqlite3 as sq
import pandas
import time
import xlsxwriter



df = []
df.append(pandas.read_csv("kospi.csv",encoding='CP949'))
#df.append(pandas.read_csv("kosdaq.csv",encoding='CP949'))
select = 0  #kospi = 0, kosdaq = 1

Sym = df[select]['Symbol']
Name = df[select]['Name']

workbook = xlsxwriter.Workbook('fng.xlsx')
worksheet = workbook.add_worksheet()

row=0
col=0


for i in range(0,len(Sym)):
    targetURL = "http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode="+Sym[i]+"&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701"
    html = urlopen(targetURL).read()
    soup = BeautifulSoup(html,'html.parser')

    try:
        fngData = soup.find("ul", {"id":"bizSummaryContent"}).getText()
        print(fngData)  
    except:
        fngData='NA'
        print("no data")

    worksheet.write(row,col,Sym[i])
    worksheet.write(row,col+1,Name[i])
    worksheet.write(row,col+2,fngData)
    row+=1

    if(i%10==0): 
        time.sleep(5)
        print("10개마다 쉬어줍시당")


workbook.close() 

