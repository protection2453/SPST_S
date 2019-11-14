#필요 라이브러리 및 파일 호출
from project_Response import *
#from WebCrawl.personal_profile import *
from tkinter import *
import tkinter.ttk
from tkinter import messagebox
import sqlite3
import pymysql
import pandas as pd
import os

length = 5
pathvar = os.path.dirname( os.path.abspath( __file__ ) ).split('\\')[2]

#데이터베이스 연결. 참고 url = https://estenpark.tistory.com/349
'''
db = pymysql.connect(host='106.10.36.206',port=27000,user='root',passwd='qwertyadmin',db='SPST_S',charset='utf8',autocommit=True)
cursor = db.cursor()
userset = pd.read_sql("SELECT * FROM user_info")
cols = list(userset)
print(userset) '''

#데이터베이스 생성
if os.path.isfile("C:/Users/"+ pathvar + "/Users.db"):
  print ("해당 파일이 있습니다. 데이터베이스를 불러옵니다.")
  conf = sqlite3.connect("C:/Users/"+ pathvar + "/Users.db")
  cursor = conf.cursor()
  userset = pd.read_sql("SELECT * FROM user_info",conf)
  cols = list(userset)
  print (userset)
else:
  print ("그런 이름의 파일은 없습니다. 새 데이터베이스를 생성합니다.")
  conf = sqlite3.connect("C:/Users/"+ pathvar + "/Users.db")
  cursor = conf.cursor() 
  cursor.execute('create table user_info(id, name, address)')
  cursor.execute('create table user_analysis(id, active_time, subject, emotion)')
  userset = pd.read_sql("SELECT * FROM user_info",conf)
  cols = list(userset)


ids = userset["id"].tolist()
nas = userset["name"].tolist()
ads = userset["address"].tolist()

lists = []
for x in range(len(ids)):
    lists.append(tuple(ids[x]))

#결과 저장
def more(text1,text2,text3):
    global treeview
    f = open("file.txt","w")
    f.write(text1+"\n")
    f.write(text2+"\n")
    f.write(text3+"\n")

    text1 = text1.replace(" ","") #공백은 결과 저장 버튼을 눌러도 저장되지 않습니다.
    text2 = text2.replace(" ","")
    text3 = text3.replace(" ","")

    values = [text1,text2,text3]
    if(len(values[0]) != 0 and len(values[1]) != 0 and len(values[2]) != 0):
        cursor.execute("insert into user_info values (?,?,?)",values)
        conf.commit()
        userset = pd.read_sql("SELECT * FROM user_info",conf)
        cols = list(userset)
    f.close()

#결과 불러오기
def grep():
    f = filedialog.askopenfilename()
    open_file = open(f, 'r')
    print(open_file.read())
    open_file.close()

#실수 종료 방지
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"): 
        root.destroy()

#사원 테이블 호출
def my_table(self):
    treeview.tag_configure("tag2", background="red")

#사원 관리
class MyFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=True)

        #id
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
        btnSave = Button(frame4, text="사원 추가",command=lambda:more(entryId.get(),entryName.get(),entryDepart.get()))
        btnSave.pack(side=LEFT, padx=10, pady=10)

#사원 관리 메인
def employee_manage():
    global x0, y0, cols, ids, nas, ads
    emplo = Toplevel(root)
    emplo.title("사원 관리")
    width2,height2 = x0,y0
    screen2_wid = root.winfo_screenwidth()
    screen2_hei = root.winfo_screenheight()
    x2 = ((screen2_wid/2) - (width2/2))
    y2 = (screen2_hei/2) - (height2/2)
    emplo.geometry('%dx%d+%d+%d' % (width2, height2, x2, y2))

    e_lbl = Label(emplo,text="사원 목록 테이블")
    e_lbl.pack()
    e_but = Label(emplo,text="My_Table")
    e_lbl.pack()

    treelists = []
    for x in range(len(ids)):
        treelist = []
        treelist.append(ids[x])
        treelist.append(nas[x])
        treelist.append(ads[x])
        treelists.append(tuple(treelist))
    print(treelists)

    treeview=tkinter.ttk.Treeview(emplo, columns=["one", "two","three"])
    treeview.column("#0", width=50)
    treeview.heading("#0",text="num") #index

    treeview.column("one", width=70)
    treeview.heading("one", text=cols[0]) #id

    treeview.column("two", width=50)
    treeview.heading("two", text=cols[1], anchor="center") #name

    treeview.column("three", width=100, anchor="w")
    treeview.heading("three", text=cols[2], anchor="center") #address

    for i in range(len(treelists)):
        treeview.insert('', 'end', text=i, values=treelists[i], iid=str(i)+"번")

    treeview.tag_bind("tag1", sequence="<<TreeviewSelect>>", callback=my_table)
    treeview.pack(side=TOP,fill=X)

    app = MyFrame(emplo)
    emplo.mainloop()

def analy_result():
    messagebox.showinfo(title='Deep Learning', message=show_newMessage())

#분석 관리
class MyFrames(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=True)

        #id
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
        btnSave = Button(frame4, text="분석 결과",command=analy_result)
        btnSave.pack(side=LEFT, padx=10, pady=10)

#분석 관리 메인
def analysis_manage():
    global x0, y0, cols, ids, nas, ads
    analys = Toplevel(root)
    analys.title("분석 관리")
    width3,height3 = x0,y0
    screen3_wid = root.winfo_screenwidth()
    screen3_hei = root.winfo_screenheight()
    x3 = ((screen3_wid/2) - (width3/2))
    y3 = (screen3_hei/2) - (height3/2)
    analys.geometry('%dx%d+%d+%d' % (width3, height3, x3, y3))

    e_lbl = Label(analys,text="분석 관리 테이블")
    e_lbl.pack()
    e_but = Label(analys,text="My_Table")
    e_lbl.pack()

    app = MyFrames(analys)
    analys.mainloop()

#메인 화면
def center_window(width=300, height=200):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

root = Tk()
x0, y0 = 800, 450
center_window(x0, y0)
root.title("메인 화면")

lbl = Label(root, text="와! 딥러닝!")
lbl.place(x=360, y = 180)

btn1 = Button(root, text="사원관리", command=employee_manage)
btn1.place(x=700, y = 340)

btn = Button(root, text="분석관리", command=analysis_manage)
btn.place(x=700, y = 380)

Button(root, text="종  료", command=on_closing).place(x=30, y = 380)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
