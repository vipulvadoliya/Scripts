#!/usr/bin/python
# -*- coding: latin-1 -*-
import os, sys
import commands
import datetime
class color:
   BOLD = '\033[1m'
   END = '\033[0m'
cr = 0
dlt = 0
flag = 0
date_format = "%Y/%m/%d"
today = datetime.date.today()
dd = 7
#dd = int(sys.argv[1])

file1 = open("deleted_servers","w")
file2 = open("created_servers","w")

file1.write("\n\nList of Deleted Servers")
file1.write("\n===================================================")
file2.write("\n\nList of Created Servers")
file2.write("\n===================================================")

f = open("server_list")
lines = f.readlines()
for line in lines:
    strg = line.split()
    if (flag == 0):
        flag = 1
        continue
    try:
        if strg[11]:
                dt1 = datetime.datetime.strptime(strg[6], date_format).date()
                diff = today - dt1
                days =  diff.days
                if (days <= dd):
                        file1.write("\n" + strg[6] + "   " + strg[10] + "   " + strg[11])
                        dlt = dlt + 1
    except:
                dt1 = datetime.datetime.strptime(strg[6], date_format).date()
                diff = today - dt1
                days = diff.days
                if (days <= dd):
                        file2.write("\n" + strg[6] + "   " + strg[10])
                        cr = cr + 1
file1.write("\n")
file2.write("\n")

f.close()
file1.close()
file2.close()

data = open("Main_File","w")
data.write("\n\n" + color.BOLD +  "Total Created Servers in Last " + str(dd) + " days : " + str(cr) + color.END + "\n")
data.write(color.BOLD +  "Total Deleted Servers in Last " + str(dd) + " days : " + str(dlt) + color.END + "\n")

f = open("created_servers")
lines = f.readlines()
for line in lines:
        data.write(line)
f.close()
f = open("deleted_servers")
lines = f.readlines()
for line in lines:
        data.write(line)
f.close()
data.close()

os.system('cat Main_File')
os.system('rm -rf Main_File')
os.system('rm -rf created_servers')
os.system('rm -rf deleted_servers')
