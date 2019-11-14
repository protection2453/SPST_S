#필요 라이브러리 및 파일 호출
from tkinter import *
import tkinter.ttk
from tkinter import messagebox
import pandas as pd
import os
import sqlite3
import platform
import sys
import pymysql

count = 0
dbs = ""

try:
    #데이터베이스 서버 연결
    conf = pymysql.connect(host='106.10.32.85', 
                        user='root', 
                        passwd='shsmsrpwhgdktjqjdlqslek!', 
                        db='SPST_S',
                        charset='utf8',
                        port=3306,
                        use_unicode=True)
    cursor = conf.cursor()
    dbs = "mysql"
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
	dbs = "sqlite"
cursor.execute("set names utf8")

def my_table(self):
	treeview.tag_configure("tag2", background="red")

	#결과 저장 - 추가
def more(text1,text2,text3):
	global count
	flag = 0

	text1 = text1.replace(" ","") #공백은 결과 저장 버튼을 눌러도 저장되지 않습니다.
	text2 = text2.replace(" ","")
	text3 = text3.replace(" ","")

	values = [text1,text2,text3]
	if(len(values[0]) != 0 and len(values[1]) != 0 and len(values[2]) != 0):
		userset = pd.read_sql("SELECT * FROM USER_INFO",conf)
		cols = list(userset)
		IDs = userset["ID"].tolist()
		nas = userset["NAME"].tolist()
		ads = userset["GROUP_NAME"].tolist()

		print(IDs,nas,ads)
		if(values[0] not in IDs):
			print("아이디 미포함")
			flag = 1
		else:
			print("아이디 포함")
			flag = 0

		if(flag==1):
			if(dbs == "mysql"):
				print(values)
				query = """INSERT INTO USER_INFO (ID,NAME,GROUP_NAME) VALUES (%s, %s, %s)"""
				cursor.execute(query,values)
			else:
				query = "INSERT INTO USER_INFO VALUES (?,?,?)"
				cursor.execute(query,values)
			conf.commit()
			userset = pd.read_sql("SELECT * FROM USER_INFO",conf)
			cols = list(userset)

			treelist = []
			treeap = treelist.append
			treeap(text1)
			treeap(text2)
			treeap(text3)

			treelists = []
			treelists.append(tuple(treelist))
			treeview.insert('', 'end', text=count, values=treelists[0], iid=str(count)+"번")
			count += 1
			complete(text1)
		else:
			notcomplete()
	else:
		notcomplete()

#결과 저장 - 제거
def grep(text1,text2,text3):
	ncount = 0
	text1 = text1.replace(" ","") #공백은 결과 저장 버튼을 눌러도 저장되지 않습니다.
	text2 = text2.replace(" ","")
	text3 = text3.replace(" ","")

	values = [text1,text2,text3]
	if(len(values[0]) != 0 and len(values[1]) != 0 and len(values[2]) != 0):
		if(values[0].lower()!="all" and values[1].lower()!="all" and values[2].lower()!="all"):
			userset = pd.read_sql("SELECT * FROM USER_INFO",conf)
			cols = list(userset)
			IDs = userset["ID"].tolist()

			for x in IDs:
				if(x == text1):
					x = text1
					break
				else:
					ncount += 1

			treeview.delete(str(ncount)+"번")

			query = "DELETE FROM USER_INFO where id = %s and name = %s and group_name = %s"
			cursor.execute(query,values)
			conf.commit()

			complete(text1)
		else:
			query = "DELETE FROM USER_INFO"
			cursor.execute(query)
			conf.commit()
			treeview.delete(*treeview.get_children())
	else:
		notcomplete()

#돌아가기
def back():	
	sys.exit()

def complete(text1):
	e_but.configure(text="My_Table - " + "changed user: "+" "+text1)

def notcomplete():
	e_but.configure(text="My_Table - " + "not changed")

#사원 관리
class MyFrame(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)
		self.master = master
		self.pack(fill=BOTH, expand=True)

		#ID
		frame1 = Frame(self)
		frame1.pack(fill=X)
		lblId = Label(frame1, text ="아이디",width=10)
		lblId.pack(side=LEFT,padx=10,pady=10)
		entryId = Entry(frame1)
		entryId.pack(fill=X, padx=10, expand=True)

		#성명
		frame2 = Frame(self)
		frame2.pack(fill=X)
		lblName = Label(frame2, text ="성명",width=10)
		lblName.pack(side=LEFT,padx=10,pady=10)
		entryName = Entry(frame2)
		entryName.pack(fill=X, padx=10, expand=True)

		#부서
		frame3 = Frame(self)
		frame3.pack(fill=X)
		lblDepart = Label(frame3, text ="부서",width=10)
		lblDepart.pack(side=LEFT,padx=10,pady=10)
		entryDepart = Entry(frame3)
		entryDepart.pack(fill=X, padx=10, expand=True)

		#저장
		frame4 = Frame(self)
		frame4.pack(fill=X)
		btnSave = Button(frame4, text="사원추가",command=lambda:more(entryId.get(),entryName.get(),entryDepart.get()))
		btnSave.pack(side=RIGHT, padx=10, pady=10)

		frame5 = Frame(self)
		frame5.pack(fill=X)
		btnDel = Button(frame5, text="사원제거",command=lambda:grep(entryId.get(),entryName.get(),entryDepart.get()))
		btnDel.pack(side=RIGHT, padx=10)

		frame6 = Frame(self)
		frame6.pack(fill=X)
		btnhID = Button(frame6, text="돌아가기",command=back)
		btnhID.pack(sid=LEFT, padx=10, pady=10)


#사원 관리 메인
global x0, y0,hIDes
emplo = Tk()
emplo.resizable(0, 0)
emplo.title("사원 관리")
x0, y0 = 820, 490
wIDth2,height2 = x0+20,y0+30
screen2_wID = emplo.winfo_screenwidth()
screen2_hei = emplo.winfo_screenheight()
x2 = ((screen2_wID/2) - (wIDth2/2))
y2 = (screen2_hei/2) - (height2/2)
emplo.geometry('%dx%d+%d+%d' % (wIDth2, height2, x2, y2))

e_lbl = Label(emplo,text="사원 목록 테이블")
e_lbl.pack()
e_but = Label(emplo,text="My_Table")
e_but.pack()

userset = pd.read_sql("SELECT * FROM USER_INFO",conf)
cols = list(userset)
IDs = userset["ID"].tolist()
nas = userset["NAME"].tolist()
ads = userset["GROUP_NAME"].tolist()

treelists = []
for x in range(len(IDs)):
	treelist = []
	treelist.append(IDs[x])
	treelist.append(nas[x])
	treelist.append(ads[x])
	treelists.append(tuple(treelist))
#print(treelists)

treeview=tkinter.ttk.Treeview(emplo, columns=["one", "two","three"])
treeview.column("#0", width=50)
treeview.heading("#0",text="num") #index
treeview.column("one", width=70, anchor="center")
treeview.heading("one", text=cols[0].lower(), anchor="center") #ID
treeview.column("two", width=50, anchor="center")
treeview.heading("two", text=cols[1].lower(), anchor="center") #NAME
treeview.column("three", width=100, anchor="center")
treeview.heading("three", text="group_name", anchor="center") #address
scroll_y = Scrollbar(emplo, orient="vertical", command=treeview.yview)
scroll_y.pack(side="right", fill="y")

for i in range(len(treelists)):
	treeview.insert('', 'end', text=i, values=treelists[i], iid=str(i)+"번")
	count += 1

treeview.tag_bind("tag1", sequence="<<TreeviewSelect>>", callback=my_table)
treeview.pack(side=TOP,fill=X)

try:
	emplo.iconbitmap(default=r'C:/Users/' + pathvar + '/Downloads/SPST_S-master/SPST_S-master/project_icon.ico')
except:
	try:
		emplo.iconbitmap(default=r'C:/Users/' + pathvar + '/Downloads/SPST_S-master/SPST_S-master/project_icon.ico')
	except:
		emplo.iconbitmap(default=r'project_icon.ico')

app = MyFrame(emplo)
emplo.mainloop()
