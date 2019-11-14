import sqlite3
import platform
from tkinter import *
import tkinter.ttk
from tkinter import messagebox
import pandas as pd
import os
import pymysql
from pprint import pprint
import subprocess

zf = 1
count = 0

try:
    #데이터베이스 서버 연결
    conf = pymysql.connect(host='106.10.32.85', 
                        user='root', 
                        passwd='shsmsrpwhgdktjqjdlqslek!', 
                        db='SPST_S',
                        charset='utf8',
                        port=3306
                        )
    cursor = conf.cursor()
except:
    #데이터베이스 로딩
    if(platform.system()=='Windows'):
    	pathvar = os.path.dirname( os.path.abspath( __file__ ) ).split('\\')[2]
    	conf = sqlite3.connect("C:/Users/"+ pathvar + "/SPST_S.db")
    	cursor = conf.cursor()
    elif(platform.system()=='Darwin'):
    	file = "SPST_S.db"
    	conf = sqlite3.connect(file)
    	cursor = conf.cursor()

def trwadding(IDs):
    global count

    usersetr = pd.read_sql("SELECT * FROM USER_RESULT where id=" + "'" + IDs + "'",conf)
    userseta = pd.read_sql("SELECT * FROM USER_ANALYSIS",conf)
    cols = list(userseta)

    ids = userseti["ID"].tolist()
    nas = userseti["NAME"].tolist()

    IDs = userseta["ID"].tolist()
    ats = userseta["ACTIVE_TIME"].tolist()
    sus = userseta["SUBJECT"].tolist()
    ems = userseta["EMOTION"].tolist()

    IDS = usersetr["ID"].tolist()
    sen = usersetr["SENTENCE"].tolist()
    ati = usersetr["TIME"].tolist()

    #chart2 append
    treelists = []
    treelist = []
    xu = len(IDs)-1
    treelist.append(IDs[xu])
    treelist.append(ats[xu])
    treelist.append(sus[xu])
    treelist.append(ems[xu])
    treelists.append(tuple(treelist))

    treeview2.insert('', 'end', text=count, values=treelists[0], iid=str(count)+"번")
    count += 1

    #chart3 append
    treelists = []
    treelist = []
    xxu = len(IDS)-1
    treelist.append(sen[xxu])
    treelist.append(ati[xxu])
    treelists.append(tuple(treelist))

    for i in range(len(treelists)):
        treeview3.insert('', 'end', values=treelists[0], iid=str(count)+"번")

    #messagebox.showinfo("your message",usersetr["SENTENCE"][len(usersetr)-1])

def inter(IDs):
    print(IDs)
    userseti = pd.read_sql("SELECT * FROM USER_INFO where id="+"'"+IDs+"'",conf)
    print(userseti)
    try:
        if(userseti["ID"][0]==IDs):
                print("\nhello")
                query = "UPDATE PERSONAL set ID=" + "'"+ IDs + "'" 
                cursor.execute(query)
                conf.commit()
                print("\nworld")
                if(zf == 0):
                    os.system("spst_analy_crawl.exe")
                    os.system("spst_result.exe")
                else:
                    subprocess.call(["python","spst_analy_crawl.py"])
                    subprocess.call(["python","spst_result.py"])
                    #try:
                    trwadding(IDs)
                    #except:
                        #messagebox.showinfo(":(","Failed..")
        else:
            messagebox.showinfo(":(",IDs+" is not in employee..")
    except pymysql.err.DataError:
        subprocess.call(["python","spst_result.py"])
        trwadding(IDs)
    except:
        messagebox.showinfo(":(",IDs+" is not in employee..")
    """
    except:
        messagebox.showinfo(":(",IDs+" error") """

def my_table(self):
	treeview.tag_configure("tag2", background="red")

#사원 관리 메인
global x0, y0,hIDes
analys= Tk()
analys.resizable(0, 0)
analys.title("훈련관리")
x0, y0 = 1150, 510
wIDth3,height3 = x0+20,y0+30
screen3_wID = analys.winfo_screenwidth()
screen3_hei = analys.winfo_screenheight()
x3 = ((screen3_wID/2) - (wIDth3/2))
y3 = (screen3_hei/2) - (height3/2)
analys.geometry('%dx%d+%d+%d' % (wIDth3, height3, x3, y3))

e_lbl = Label(analys,text="훈련 관리 테이블")
e_lbl.pack()
e_but = Label(analys,text="My_Table")
e_but.pack()

userseti = pd.read_sql("SELECT * FROM USER_INFO",conf)
userlist = list(userseti["ID"])

userseta = pd.read_sql("SELECT * FROM USER_ANALYSIS",conf)
cols = list(userseta)

usersetr = pd.read_sql("SELECT * FROM USER_RESULT",conf)

ids = userseti["ID"].tolist() #table 1
nas = userseti["NAME"].tolist()

IDs = userseta["ID"].tolist() #table 2
ats = userseta["ACTIVE_TIME"].tolist()
sus = userseta["SUBJECT"].tolist()
ems = userseta["EMOTION"].tolist()

IDS = usersetr["ID"].tolist()
sen = usersetr["SENTENCE"].tolist()
ati = usersetr["TIME"].tolist()

treeview1=tkinter.ttk.Treeview(analys, columns=["one","two"],height="15")#===========여기
treeview1.column("#0", width=0)
treeview1.column("one", width=100,anchor="center")
treeview1.heading("one", text="Id",anchor="center") #ID
treeview1.column("two", width=100,anchor="center")
treeview1.heading("two", text="Name",anchor="center") #name

treelists = []
for x in range(len(ids)):
    treelist = []
    treelist.append(ids[x])
    treelist.append(nas[x])
    treelists.append(tuple(treelist))

for i in range(len(treelists)):
    treeview1.insert('', 'end', values=treelists[i], iid=str(i)+"번")
treeview1.tag_bind("tag1", sequence="<<TreeviewSelect>>", callback=my_table)

treeview2=tkinter.ttk.Treeview(analys, columns=["one", "two","three","four"],height="15")
treeview2.column("#0", width=50)
treeview2.heading("#0",text="num") #index
treeview2.column("one", width=100,anchor="center")
treeview2.heading("one", text=cols[0].lower(),anchor="center") #ID
treeview2.column("two", width=50,anchor="center")
treeview2.heading("two", text="time",anchor="center") #active time
treeview2.column("three", width=80,anchor="center")
treeview2.heading("three", text=cols[2].lower(),anchor="center") #subject
treeview2.column("four", width=80, anchor="center")
treeview2.heading("four", text=cols[3].lower(), anchor="center") #emotion

treelists = []
for x in range(len(IDs)):
    treelist = []
    treelist.append(IDs[x])
    treelist.append(ats[x])
    treelist.append(sus[x])
    treelist.append(ems[x])
    treelists.append(tuple(treelist))

for i in range(len(treelists)):
    treeview2.insert('', 'end', text=i, values=treelists[i], iid=str(i)+"번")
    count += 1

treeview2.tag_bind("tag1", sequence="<<TreeviewSelect>>", callback=my_table)

treeview3=tkinter.ttk.Treeview(analys, columns=["one","two"],height="15")#===========여기
treeview3.column("#0", width=0)
treeview3.column("one",width=350,anchor="center")
treeview3.heading("one",text="sentence") #sentence
treeview3.column("two", width=180,anchor="center")
treeview3.heading("two", text="time",anchor="center") #anaysis time

treelists = []
for x in range(len(IDS)):
    treelist = []
    treelist.append(sen[x])
    treelist.append(ati[x])
    treelists.append(tuple(treelist))

for i in range(len(treelists)):
    treeview3.insert('', 'end', values=treelists[i], iid=str(i)+"번")

treeview1.pack(side="left", anchor="nw", padx="15")#===========여기
treeview2.pack(side="left", anchor="n", padx="10")#===========여기
treeview3.pack(side="left", anchor="ne", padx="10")#===========여기

#입력
lblId = Label(analys, text ="분석할 아이디",width=10)
lblId.place(x=25,y=400)
entryId = Entry(analys)
entryId.place(x=120,y=400,width=1000)

#훈련
btanaly = Button(analys, text="훈련 시작",command=lambda:inter(entryId.get()))
btanaly.place(x=1050,y=450)

try:
	analys.iconbitmap(default='C:/Users/' + pathvar + '/Downloads/SPST_S-master/project_icon.ico')
except:
	analys.iconbitmap(default='project_icon.ico')

analys.mainloop()