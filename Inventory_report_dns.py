#!/usr/bin/python
# -*- coding: latin-1 -*-
#importing os and date related packages
import os, sys
import commands
import datetime
import time

#cosmatic purpose
class color:
   BOLD = '\033[1m'
   END = '\033[0m'

#storing current/today's date in one variable
today = datetime.date.today()

#variable which we use the count date diff, between current and server created/deleted.
dt1=10000
#dd = 7
#storing command line argument of days
dd = int(sys.argv[1])
#storing the date in string format, from the gitlab log file
tst="empty"
#Created server and deleted server counter
serv_created=0
serv_deleted=0

#date_convert function, which convert string date to date data type, and then return the number of days diff betweed current date and server creation/deletion date.
def date_convert(str_date):
        conv=time.strptime(str_date,"%a %b %d %Y")
        tmp = time.strftime("%Y-%m-%d",conv)
        tst2 = datetime.datetime.strptime(tmp, '%Y-%m-%d').date()
        diff = today - tst2
        days =  diff.days
        return days

#downloading the Repo from the gitlab
os.system('git clone https://github.com/vipulvadoliya/Scripts.git')
#changing the directory
os.chdir('/root/srini_inventory/Scripts')
#generating the log file from the inventory
os.system('git log -p generic-machines.inc > new_inventory_log')
#filtering the date, added server and deleted server lines and store into seprate file
os.system('egrep "^Date|^\+s|^-s" new_inventory_log > inventory_log_updated')
#copy the inventory_log_updated file to home directory
os.system('cp inventory_log_updated /root/srini_inventory/')
#changing the directory
os.chdir('/root/srini_inventory/')
#removing the repo from local directory, because we have got the required log file.
os.system('rm -rf Scripts')


#storing created servers and deleted servers in seprate file.
file1 = open("created_servers","w")
file2 = open("deleted_servers","w")

file1.write("\n\nList of Created Servers")
file1.write("\n===================================================")
file2.write("\n\nList of Deleted Servers")
file2.write("\n===================================================")

#opening the inventory_log_updated file and fatch the created servers, deleted servers withing the numbers of days.
f = open("inventory_log_updated")
lines = f.readlines()
for line in lines:
    strg = line.split()
    try:
#       Checking if the line in log file is containing date or not ?
        if (strg[0] == "Date:"):
                #getting day=strg[1]=Fri month=strg[2]=Feb date=strg[3]=23 year=strg[5]=2018 as a string, not date data type.
                tst = strg[1] +" "+ strg[2] +" "+ strg[3] +" "+ strg[5]
                #calling the date_convert function and passing the string date which we got from the log file as a argument
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
