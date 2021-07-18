from tkinter import*
import tkinter as tk
import tkinter.messagebox

def TestPage():
    global usrval
    global testing
    testing = True
    # 获取题目
    global Questions  # 题目
    Questions = readQuestion()
    # 当前题目号
    global curQues
    # 考试的答案
    global ansArray
    # 初始化
    ansArray = []
    curQues = 1
    time = 2*60*60
    #主窗口
    Window = Tk()
    Window.geometry('950x700+300+50')
    Window.resizable(width=False,height=False)
    Window.title("考试中")
    # 切换题目按钮
    QuesLable = Label(Window, text=f'题目：{curQues}', font=('console', 20))
    QuesLable.place(x=10, y=60)
    nextBut = Button(Window, text="Next->", font=('console', 20),
                     command=lambda: ToNextQues(len(Questions), QuesLable, queframe))
    nextBut.place(x=790, y=50)
    lastBut = Button(Window, text="<-Last", font=('console', 20), command=lambda: ToLastQues(QuesLable, queframe))
    lastBut.place(x=650, y=50)
    # 结束考试按钮
    EndTestBtn = Button(Window, text='结束考试', font=('console', 20), command=lambda: endTest(EndTestBtn, Window))
    EndTestBtn.place(x=800, y=600)
    #以下为倒计时模块
    lable = Label(Window,text="考试时间倒计时：",font=('console',20))
    lable.place(x=10,y=10)
    hour = int(time/3600)
    minute = int((time-hour*3600)/60)
    second = int(time-hour*3600-minute*60)
    countDown = Label(Window,text=f'{hour}:{minute}:{second}',font=('console',20),fg='red')
    countDown.place(x=210,y=10)
    #时间倒计时函数
    def countTime():
        nonlocal time,hour,minute,second
        time -= 1
        #时间到，自动结束考试
        if time < 1:
            while len(ansArray) < len(Questions):
                ansArray.append('')
            endTest(EndTestBtn, Window)
        hour = int(time / 3600)
        minute = int((time - hour * 3600) / 60)
        second = int(time - hour * 3600 - minute * 60)
        countDown.config(text=f'{hour}:{minute}:{second}')
        if testing:
            countDown.after(1000, countTime)
    countDown.after(1000,countTime)
    #——————————————————————————————
    #考生信息，即名字
    Info = Label(Window,text=f'姓名：{usrval.get()}',font=('console',20))
    Info.place(x= 700,y=10)
    #——————————————————————————————
    #题目显示区域
    queframe = Frame(Window,width=930,height=500,bd=3,relief=GROOVE)
    queframe.place(x=10,y=100)
    #显示题目信息函数
    ShowQuestons(queframe)
    Window.mainloop()

#记录考生答案函数
def SetAns(StringVar):
    if curQues > len(ansArray):
        ansArray.append(StringVar.get())
    else:
        ansArray[curQues-1] = StringVar.get()

#显示题目信息函数
def ShowQuestons(Frame):
    if Questions[curQues-1]["type"] == 1: #选择题
        for widget in Frame.winfo_children():
            widget.destroy()
        #显示题目描述
        QLable = Label(Frame,text=f'{Questions[curQues-1]["des"]}',font=('console', 20))
        QLable.place(x=20,y=70)
        ans = StringVar()
        #设置显示的答案
        if len(ansArray) < curQues or ansArray[curQues-1] == '':
            ans.set('A')#默认选择A
        else:
            ans.set(ansArray[curQues-1])
        #显示4个选项
        Radiobutton(Frame,text=f'{Questions[curQues-1]["choice"][0]}',variable=ans,value='A',font=('console',20),command=lambda:SetAns(ans)).place(x=30,y=200)
        Radiobutton(Frame,text=f'{Questions[curQues-1]["choice"][1]}',variable=ans,value='B',font=('console',20),command=lambda:SetAns(ans)).place(x=500,y=200)
        Radiobutton(Frame,text=f'{Questions[curQues-1]["choice"][2]}',variable=ans,value='C',font=('console',20),command=lambda:SetAns(ans)).place(x=30,y=300)
        Radiobutton(Frame,text=f'{Questions[curQues-1]["choice"][3]}',variable=ans,value='D',font=('console',20),command=lambda:SetAns(ans)).place(x=500,y=300)
    if Questions[curQues-1]["type"] == 2: #判断题
        for widget in Frame.winfo_children():
            widget.destroy()
        # 显示题目描述
        QLable = Label(Frame, text=f'{Questions[curQues-1]["des"]}', font=('console', 20))
        QLable.place(x=20, y=70)
        ans = StringVar()
        # 设置显示的答案
        if len(ansArray) < curQues or ansArray[curQues - 1] == '':
            ans.set('正确')  # 默认选择正确
        else:
            ans.set(ansArray[curQues - 1])
        # 显示2个选项
        Radiobutton(Frame, text=f'{Questions[curQues - 1]["choice"][0]}', variable=ans, value='正确', font=('console', 20),
                    command=lambda: SetAns(ans)).place(x=30, y=200)
        Radiobutton(Frame, text=f'{Questions[curQues - 1]["choice"][1]}', variable=ans, value='错误', font=('console', 20),
                    command=lambda: SetAns(ans)).place(x=500, y=200)
    if Questions[curQues-1]["type"] == 3: #填空题
        for widget in Frame.winfo_children():
            widget.destroy()
        # 显示题目描述
        QLable = Label(Frame, text=f'{Questions[curQues-1]["des"]}', font=('console', 20))
        QLable.place(x=20, y=70)
        ans = StringVar()
        # 设置显示的答案
        if len(ansArray) < curQues or ansArray[curQues - 1] == '':
            ans.set('') #默认为空
        else:
            ans.set(ansArray[curQues - 1])
        #填空框和确认答案按钮
        Writeques = Entry(Frame, textvariable=ans)
        Writeques.place(x=300, y=300)
        subButton = Button(Frame,text='确定',font=('console', 10),command=lambda:SetAns(ans))
        subButton.place(x=450, y=300)

#切换下个题目的按钮
def ToNextQues(TotalNum,Lable,Frame):
    global curQues
    #每个题必须作答后才能做下个题目
    if len(ansArray) < curQues:
        tk.messagebox.showerror('错误','请做出选择/填写答案，再做下一个题！！')
    else:
        if curQues < TotalNum:
            curQues += 1
            Lable.config(text=f'题目：{curQues}')
    ShowQuestons(Frame)

#切换上个题目的函数
def ToLastQues(Lable,Frame):
    global curQues
    if curQues > 1:
        curQues -= 1
        Lable.config(text=f'题目：{curQues}')
    ShowQuestons(Frame)

#从文件中读取题目信息
def readQuestion():
    file = open('questions.txt',encoding='utf-8')
    data = file.readlines()
    ques = []
    for i in range(len(data)):
        ques.append(eval(data[i]))
    return ques

#考试结束函数
def endTest(Button,window):
    global score
    global testing
    score = 0
    #先判断是否作答完毕
    if len(ansArray)<len(Questions):
        tk.messagebox.showerror('错误', '你还没做完题目！！')
    else:
        #计算分数
        for i in range(len(ansArray)):
            if ansArray[i] == Questions[i]['ans']:
                score +=10
        #停止计时
        testing = False
        #设置不可提交答案，即主动结束考试
        Button.config(state='disabled')
        #显示分数
        Label(window,text=f'得分：{score}',font=('console', 20)).place(x=50,y=600)

def usr_login():
    Register.destroy()
    TestPage()
#——————————————————————————
#登录界面
Register = Tk()
usrval = StringVar()
pasaval = StringVar()
Register.geometry('400x200+500+200')
Register.resizable(0,0)
Register.title('考试系统')
#用户名和密码
usrLab = Label(Register,text='username:',font=('console',15))
usrLab.place(x=70,y=50)
usrPut = Entry(Register,textvariable=usrval)
usrPut.place(x=170,y=50)
password = Label(Register,text='password:',font=('console',15))
password.place(x=70,y=80)
passwordPut = Entry(Register,textvariable=pasaval,show='*')
passwordPut.place(x=170,y=80)
#登录按钮
loginBtn = Button(Register,text='login',command=lambda:usr_login()).place(x=190,y=120)
Register.mainloop()
