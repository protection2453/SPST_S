from tkinter import *
from Deep.project_Response import *
from tkinter.messagebox import showinfo


if __name__ == "__main__":
    def analysis():
        showinfo(title='Deep Learning', message=show_newMessage())
        #print("%s", show_newMessage())

def center_window(width=300, height=200):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

root = Tk()
center_window(300, 150)
root.title("Deep Learning")

btn1 = Button(root, text="사원관리", command=analysis)
btn1.place(x=235, y = 90)

btn = Button(root, text="분석관리", command=analysis)
btn.place(x=235, y = 120)

while True:
    Button(root, text="종  료", command=quit).place(x=10, y = 120)
    root.mainloop()


