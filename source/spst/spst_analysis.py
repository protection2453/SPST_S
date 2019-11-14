import sqlite3
import platform
from tkinter import *
import tkinter.ttk
from tkinter import messagebox
import pandas as pd
import os
import pymysql

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

def inter(IDs):
    print(IDs)
    userset = pd.read_sql("SELECT * FROM USER_INFO where id="+"'"+IDs+"'",conf)
    print(userset)
    try:
        if(userset["ID"][0]==IDs):
                query = "UPDATE PERSONAL set ID=" + "'"+ IDs + "'" 
                cursor.execute(query)
                conf.commit()
                os.system("spst_analy_crawl.exe")
        else:
            messagebox.showinfo(":(",IDs+" is not in employee..")
    except:
        messagebox.showinfo(":(",IDs+" is not in employee..")
    #os.system("spst_result.exe")

def my_table(self):
	treeview.tag_configure("tag2", background="red")

#훈련 관리
class MyFrames(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.pack(side="left", anchor="s", expand=True)

        #ID
        frame1 = Frame(self)
        frame1.pack(side="left",anchor="sw")
        lblId = Label(frame1, text ="분석할 아이디",width=10)
        lblId.pack(side="left",anchor="s")
        entryId = Entry(frame1)
        entryId.pack(padx=10, expand=True)

        #훈련
        frame2 = Frame(self)
        frame2.pack(side="left",anchor="se")
        btanaly = Button(frame2, text="훈련 시작",command=lambda:inter(entryId.get()))
        btanaly.pack(padx=10,pady=10)


#사원 관리 메인
global x0, y0,hIDes
analys= Tk()
analys.resizable(0, 0)
analys.title("훈련관리")
x0, y0 = 1200, 490
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

ids = userseti["ID"].tolist()
nas = userseti["NAME"].tolist()
IDs = userseta["ID"].tolist()
ats = userseta["ACTIVE_TIME"].tolist()
sus = userseta["SUBJECT"].tolist()
ems = userseta["EMOTION"].tolist()

'''
treeview=tkinter.ttk.Treeview(analys, columns=["one", "two"])
treeview.column("#0", width=50)
treeview.heading("#0",text="num") #index
treeview.column("one", width=100,anchor="center")
treeview.heading("one", text=cols[0].lower(),anchor="center") #ID
treeview.column("two", width=50,anchor="center")
treeview.heading("two", text="name",anchor="center") #name

treelists = []
for x in range(len(ids)):
    treelist = []
    treelist.append(ids[x])
    treelist.append(nas[x])
    treelists.append(tuple(treelist))

for i in range(len(treelists)):
    treeview.insert('', 'end', text=i, values=treelists[i], iid=str(i)+"번")

treeview.tag_bind("tag1", sequence="<<TreeviewSelect>>", callback=my_table)
treeview.pack(side="top",fill="x")'''

treeview1=tkinter.ttk.Treeview(analys, columns=["one"])
treeview1.column("#0", width=50)
treeview1.heading("#0",text="num") #index

treeview2=tkinter.ttk.Treeview(analys, columns=["one", "two","three","four"])
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
#treeview2.height(5)

treeview3=tkinter.ttk.Treeview(analys, columns=["one"])
treeview3.column("#0", width=50)
treeview3.heading("#0",text="num") #index


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

treeview2.tag_bind("tag1", sequence="<<TreeviewSelect>>", callback=my_table)
treeview1.pack(side="left", anchor="nw", padx="10")
treeview2.pack(side="left", anchor="n", padx="10")
treeview3.pack(side="left", anchor="ne", padx="10")

try:
	analys.iconbitmap(default='C:/Users/' + pathvar + '/Downloads/SPST_S-master/project_icon.ico')
except:
	analys.iconbitmap(default='project_icon.ico')

app = MyFrames(analys)
analys.mainloop()
