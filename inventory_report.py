#!/usr/bin/python
# -*- coding: latin-1 -*-
import os, sys
import commands
import datetime
import time                
class color:
   BOLD = '\033[1m'
   END = '\033[0m'
today = datetime.date.today()
dt1=10000
#dd = 7
dd = int(sys.argv[1])
tst="empty"
serv_created=0
serv_deleted=0
def date_convert(str_date):
	conv=time.strptime(str_date,"%a %b %d %Y")
	tmp = time.strftime("%Y-%m-%d",conv)
	tst2 = datetime.datetime.strptime(tmp, '%Y-%m-%d').date()
	diff = today - tst2
        days =  diff.days
	return days

os.system('git clone https://gitlab.com/vipulvadoliya/Test.git')
os.chdir('/root/script/Test')
os.system('git log -p server_inventory > new_inventory_log')
os.system('egrep "^Date|^\+s|^-s" new_inventory_log > inventory_log_updated')
os.system('cp inventory_log_updated /root/script/')
os.chdir('/root/script')
os.system('rm -rf Test')

file1 = open("created_servers","w")
file2 = open("deleted_servers","w")

file1.write("\n\nList of Created Servers")
file1.write("\n===================================================")
file2.write("\n\nList of Deleted Servers")
file2.write("\n===================================================")

f = open("inventory_log_updated")
lines = f.readlines()
for line in lines:
    strg = line.split()
    try:
        if (strg[0] == "Date:"):
		tst = strg[1] +" "+ strg[2] +" "+ strg[3] +" "+ strg[5]
		dt1 = date_convert(tst)

	else:
		lst1 = list(strg[0])
		str_cmp = lst1[0] + lst1[1]
		if str_cmp == "+s":
			if dt1 <= dd:
				serv_created=serv_created+1;
				file1.write("\n" + strg[0].strip("+"))

		if str_cmp == "-s":
			if dt1 <= dd:
				serv_deleted=serv_deleted+1;
				file2.write("\n" + strg[0].strip("-"))

    except:
	print "in exception"

file1.write("\n")
file2.write("\n")
f.close()
file1.close()
file2.close()

data = open("Main_File","w")
data.write("\n\n" + color.BOLD +  "Total Created Servers in Last " + str(dd) + " days : " + str(serv_created) + color.END + "\n")
data.write(color.BOLD +  "Total Deleted Servers in Last " + str(dd) + " days : " + str(serv_deleted) + color.END + "\n")

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
os.system('rm -rf inventory_log_updated')
os.system('rm -rf created_servers')
os.system('rm -rf deleted_servers')
