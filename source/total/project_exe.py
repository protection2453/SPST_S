#필요 라이브러리 및 파일 호출
from tkinter import *
import tkinter.ttk
from tkinter import messagebox
import sqlite3
import pandas as pd
import os
import time
from PIL import Image

from project_Response import *
from personal_json import *
from personal_data import *
from personal_topic import *
from feeling_to_data import *
from personal_feeling import *
from personal_profile import *

pathvar = os.path.dirname( os.path.abspath( __file__ ) ).split('\\')[2]

#데이터베이스 생성
if os.path.isfile("C:/Users/"+ pathvar + "/Users.db"):
  print ("해당 파일이 있습니다. 데이터베이스를 불러옵니다.")
  conf = sqlite3.connect("C:/Users/"+ pathvar + "/Users.db")
  cursor = conf.cursor()
  userset = pd.read_sql("SELECT * FROM user_info",conf)
  userlist = pd.read_sql("SELECT * FROM user_info",conf)
  userlist = list(userlist["id"])
  cols = list(userset)
  print (userset)
else:
  print ("그런 이름의 파일은 없습니다. 새 데이터베이스를 생성합니다.")
  conf = sqlite3.connect("C:/Users/"+ pathvar + "/Users.db")
  cursor = conf.cursor() 
  cursor.execute('create table user_info(id, name, address)')
  cursor.execute('create table user_analysis(id, active_time, subject, emotion)')
  userset = pd.read_sql("SELECT * FROM user_info",conf)
  userlist = pd.read_sql("SELECT * FROM user_info",conf)
  userlist = list(userlist["id"])
  cols = list(userset)

ids = userset["id"].tolist()
nas = userset["name"].tolist()
ads = userset["address"].tolist()

lists = []
for x in range(len(ids)):
    lists.append(tuple(ids[x]))

#결과 저장 - 추가
def more(text1,text2,text3):
    text1 = text1.replace(" ","") #공백은 결과 저장 버튼을 눌러도 저장되지 않습니다.
    text2 = text2.replace(" ","")
    text3 = text3.replace(" ","")

    values = [text1,text2,text3]
    if(len(values[0]) != 0 and len(values[1]) != 0 and len(values[2]) != 0):
        cursor.execute("insert into user_info values (?,?,?)",values)
        conf.commit()
        userset = pd.read_sql("SELECT * FROM user_info",conf)
        cols = list(userset)

#결과 저장 - 제거
def grep(text1,text2,text3):
    text1 = text1.replace(" ","") #공백은 결과 저장 버튼을 눌러도 저장되지 않습니다.
    text2 = text2.replace(" ","")
    text3 = text3.replace(" ","")

    values = [text1,text2,text3]
    print(type(text1))
    if(len(values[0]) != 0 and len(values[1]) != 0 and len(values[2]) != 0):
        query = "DELETE FROM 'user_info' where id =" + "'" + text1 + "'" + "and name =" + "'" + text2 + "'" + "and address =" + "'" + text3 + "'"
        cursor.execute(query)
        conf.commit()
        userset = pd.read_sql("SELECT * FROM user_info",conf)
        cols = list(userset)

#실수 종료 방지
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"): 
        root.destroy()

#사원 테이블 호출
def my_table(self):
    treeview.tag_configure("tag2", background="red")

#창 숨기기
def hide():
    root.withdraw()

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
        btnSave = Button(frame4, text="사원추가",command=lambda:more(entryId.get(),entryName.get(),entryDepart.get()))
        btnSave.pack(side=RIGHT, padx=10, pady=10)

        frame5 = Frame(self)
        frame5.pack(fill=X)
        btnDel = Button(frame5, text="사원제거",command=lambda:grep(entryId.get(),entryName.get(),entryDepart.get()))
        btnDel.pack(side=RIGHT, padx=10, pady=10)

        frame6 = Frame(self)
        frame6.place(x=30, y = 440)
        btnhid = Button(frame6, text="돌아가기",command=hide)
        btnhid.place(x=30, y = 440)

#사원 관리 메인
def employee_manage():
    global x0, y0,hides
    emplo = Toplevel(root)
    emplo.resizable(0, 0)
    emplo.title("사원 관리")
    width2,height2 = x0+20,y0+30
    screen2_wid = root.winfo_screenwidth()
    screen2_hei = root.winfo_screenheight()
    x2 = ((screen2_wid/2) - (width2/2))
    y2 = (screen2_hei/2) - (height2/2)
    emplo.geometry('%dx%d+%d+%d' % (width2, height2, x2, y2))

    userset = pd.read_sql("SELECT * FROM user_info",conf)
    cols = list(userset)
    ids = userset["id"].tolist()
    nas = userset["name"].tolist()
    ads = userset["address"].tolist()

    e_lbl = Label(emplo,text="사원 목록 테이블")
    e_lbl.pack()
    e_but = Label(emplo,text="My_Table")
    e_but.pack()

    treelists = []
    for x in range(len(ids)):
        treelist = []
        treelist.append(ids[x])
        treelist.append(nas[x])
        treelist.append(ads[x])
        treelists.append(tuple(treelist))
    #print(treelists)

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


user_profile = 0

#분석 시작
def interactive(text1):
    global user_profile
    def f1(x):
        return resultk[x]

    userlist = pd.read_sql("SELECT * FROM user_info",conf)
    userlist = list(userlist["id"])

    text1 = text1.replace(" ","")
    if(len(text1) != 0):
        for user in userlist:
            if(text1 == user):
                #try:
                main(text1)
                personal_set = (personal_datas(text1))
                #주로 활동하는 시간 파악
                arrs = list(personal_set["user_time"])
                isarr = [int((((arrs[x].split())[1].split(":"))[0])) for x in range(len(arrs))]
                resultk = Counter(isarr)
                key_max = max(resultk.keys(), key=f1)

                #빈도수 바탕 주제 분석 - 형태소 분리
                arr2 = list(personal_set["user_message"])
                #print(arr2)
                lenarr2 = len(arr2)

                data = ""
                for x in range(lenarr2):
                    data += arr2[x]
                    iH = isHangul(data)

                parses = datapaser(data) 
                fword,fnumber = express(parses)
                pointlist = []
                if iH:
                    reduceword = ['뉴콘']
                    for x in reduceword:
                        if(fword[0] == x):
                            pointword = '콘서트'
                        else:
                            pointword = fword[0]
                            pointlist.append(pointword)
                            pointlist.append(fnumber[0])
                else:
                    pointlist.append("한글 아님")
                    pointlist.append("None")
                    fword.append("None")
                fxs = [i for i, _ in enumerate(fword)]
                exceling()
                #빈도수 바탕 주제 분석 - 감정 분석 밑바탕 파일
                f = open("train_docs.txt","w",encoding='utf-8')
                data = arr2[0]
                pprint(arr2[0])
                f.write(str(data))
                f.close()

                f_test = open('train_docs.txt','r',encoding='UTF-8')
                emot = mainfeel(f_test)
                user_profile = profiling(text1,key_max,pointlist,iH,fword,emot)
                analy_result(user_profile)

                values = [user_profile["id"][0],user_profile["time"][0],user_profile["user_topic"][0],user_profile["emotion"][0]]
                cursor.execute("insert into user_analysis values (?,?,?,?)",values)
                conf.commit()
                userset = pd.read_sql("SELECT * FROM user_analysis",conf)
                cols = list(userset)

                #except Exception as ex:
                #    print("None information",ex)
    else:
        messagebox.showinfo(title="Web Crawlling",message="입력 후 버튼을 눌러주세요.")

#훈련 결과
def analy_result(userdata):
    print(userdata)
    print(userdata["user_topic"][0])
    messagebox.showinfo(title='Deep Learning', message=show_newMessage(userdata["user_topic"][0]))

def show_newMessage(topicdata):
    changelist = ['콘서트','공연장','스포츠','공연','표','암표','재관','티켓팅']
    for x in changelist:
        if(x == topicdata):
            topicdata = 티켓
            message = topicdata+" "+"구하는법"

    message = "티켓 구하는법"
    return make_reply(message)

    message = ""
    new_message = make_reply(message)

#훈련 관리
class MyFrames(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=True)

        #목록
        frame1 = Frame(self)
        frame1.pack(fill=X)
        IblLi = Label(frame1, text="사원 목록: "+str(userlist))
        IblLi.pack()

        #id
        frame2 = Frame(self)
        frame2.pack(fill=X)
        lblId = Label(frame2, text ="분석할 아이디",width=10)
        lblId.pack(side=LEFT,padx=10,pady=10)
        entryId = Entry(frame2)
        entryId.pack(fill=X, padx=10, expand=True)

        #훈련
        frame3 = Frame(self)
        frame3.pack(fill=X)
        btanaly = Button(frame3, text="훈련 시작",command=lambda:interactive(entryId.get()))
        btanaly.pack(side=RIGHT, padx=10,pady=10)

#훈련 관리 메인
def analysis_manage():
    global x0, y0
    analys = Toplevel(root)
    analys.resizable(0, 0)
    analys.title("훈련 관리")
    width3,height3 = x0+20,y0+30
    screen3_wid = root.winfo_screenwidth()
    screen3_hei = root.winfo_screenheight()
    x3 = ((screen3_wid/2) - (width3/2))
    y3 = (screen3_hei/2) - (height3/2)
    analys.geometry('%dx%d+%d+%d' % (width3, height3, x3, y3))

    userlist = pd.read_sql("SELECT * FROM user_info",conf)
    userlist = list(userlist["id"])

    userset = pd.read_sql("SELECT * FROM user_analysis",conf)
    cols = list(userset)

    ids = userset["id"].tolist()
    ats = userset["active_time"].tolist()
    sus = userset["subject"].tolist()
    ems = userset["emotion"].tolist()

    e_lbl = Label(analys,text="훈련 관리 테이블")
    e_lbl.pack()
    e_but = Label(analys,text="My_Table")
    e_but.pack()

    treeview=tkinter.ttk.Treeview(analys, columns=["one", "two","three","four"])
    treeview.column("#0", width=50)
    treeview.heading("#0",text="num") #index
    treeview.column("one", width=70,anchor="w")
    treeview.heading("one", text=cols[0],anchor="center") #id
    treeview.column("two", width=50,anchor="w")
    treeview.heading("two", text=cols[1],anchor="center") #active time
    treeview.column("three", width=100,anchor="w")
    treeview.heading("three", text=cols[2],anchor="center") #subject
    treeview.column("four", width=100, anchor="w")
    treeview.heading("four", text=cols[3], anchor="center") #emotion

    treelists = []
    for x in range(len(ids)):
        treelist = []
        treelist.append(ids[x])
        treelist.append(ats[x])
        treelist.append(sus[x])
        treelist.append(ems[x])
        treelists.append(tuple(treelist))

    for i in range(len(treelists)):
        treeview.insert('', 'end', text=i, values=treelists[i], iid=str(i)+"번")

    treeview.tag_bind("tag1", sequence="<<TreeviewSelect>>", callback=my_table)
    treeview.pack(side=TOP,fill=X)

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
root.resizable(0, 0)
x0, y0 = 820, 490
center_window(x0, y0)
root.title("메인 화면")
root.iconbitmap(default=r'C:/Users/' + pathvar + '/Downloads/SPST_S-master/SPST_S-master/project_icon.ico')

image = Image.open("logo.gif") #창 크기에 맞게 이미지 크기 조절
resize_image = image.resize((x0,y0))
resize_image.save('logo.gif')
images = PhotoImage(file = "logo.gif") #이미지 배치
lbl = Label(root, image=images)
lbl.pack(side="bottom",fill="both",expand="True")

btn1 = Button(root, text="사원관리", command=employee_manage)
btn1.place(x=700, y = 400)

btn = Button(root, text="훈련관리", command=analysis_manage)
btn.place(x=700, y = 440)

Button(root, text="종   료", command=on_closing).place(x=30, y = 440)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
