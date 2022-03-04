import json
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox

from MyTk import MyTk
from paper import Paper
from question import paperBegin


class InitialInterface(MyTk):
    def __init__(self):
        super().__init__()

        self.label = Label(self.frame, text='欢迎来到 Q&A platform for Python\n',
                           font=('微软雅黑', 20, 'bold'))
        self.label.pack()

        self.loginButton = Button(self.frame, text='登录', command=self.createLogin,
                                  font=('微软雅黑', 12))
        self.loginButton.pack()

        self.loginButton = Button(self.frame, text='注册', command=self.createRegister,
                                  font=('微软雅黑', 12))
        self.loginButton.pack()

        self.Win.mainloop()

    def createLogin(self):
        Login(self.Win)

    def createRegister(self):
        Register()


class Login(MyTk):
    def __init__(self, win1):
        super().__init__()

        self.winToDestroy = win1

        label = Label(self.frame, text='登录Q&A platform for Python',
                      font=('微软雅黑', 16, 'bold'))
        label.pack()

        label1 = Label(self.frame, text='手机号码',
                       font=('微软雅黑', 12))
        label1.pack()
        self.user_phoneNumber = Entry(self.frame)
        self.user_phoneNumber.pack()

        label2 = Label(self.frame, text='密码',
                       font=('微软雅黑', 12))
        label2.pack()
        self.user_code = Entry(self.frame, show='*')
        self.user_code.pack()

        self.registerButton = Button(self.frame, text='登录', command=self.createLogin,
                                     font=('微软雅黑', 12))
        self.registerButton.pack()

        self.Win.mainloop()

    def createLogin(self):
        phoneNumber = self.user_phoneNumber.get() or ' '
        if not phoneNumber.isdigit():
            messagebox.showinfo('登录提示', '您好, 请注册一个答题账号')

        code = self.user_code.get()

        file = "D:\pyHomework/topInformation.txt"
        registered = False
        with open(file) as fp:
            for line in fp:
                if (line.split(" "))[0] == phoneNumber:
                    if (line.split(" "))[1] == code:
                        self.createTestChoose(line.split(" ")[2], phoneNumber)
                        registered = True
                        break
                    else:
                        messagebox.showinfo('登录提示', '用户 %s 您好, 请重新检查你的密码' % (line.split(" ")[2]))
                        registered = True
                        break
            if not registered:
                messagebox.showinfo('登录提示', '您好, 请注册一个答题账号')

    def createTestChoose(self, name, people):
        self.Win.destroy()
        self.winToDestroy.destroy()
        LoginSuccess(name, people)


class Choose(MyTk):
    def __init__(self, people):
        super().__init__()
        screenwidth = self.Win.winfo_screenwidth()
        screenheight = self.Win.winfo_screenheight()
        width = 700
        height = screenheight - 100
        alignStr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 4)
        self.Win.geometry(alignStr)
        self.frame.pack()
        label = Label(self.frame, text='选择题目',
                      font=('微软雅黑', 16, "bold"))
        label.pack()
        frameF = Frame(self.frame)
        frameF.pack()
        frameName = Frame(frameF)
        frameName.pack(side=LEFT)
        Label(frameName, text='\nsingle choice easy\n', font=('微软雅黑', 11)).pack()
        Label(frameName, text='single choice normal\n', font=('微软雅黑', 11)).pack()
        Label(frameName, text='single choice hard\n', font=('微软雅黑', 11)).pack()
        Label(frameName, text='true or false easy\n', font=('微软雅黑', 11)).pack()
        Label(frameName, text='true or false normal\n', font=('微软雅黑', 11)).pack()
        Label(frameName, text='true or false hard\n', font=('微软雅黑', 11)).pack()
        Label(frameName, text='short answer question easy\n', font=('微软雅黑', 11)).pack()
        Label(frameName, text='short answer question normal\n', font=('微软雅黑', 11)).pack()
        Label(frameName, text='short answer question hard', font=('微软雅黑', 11)).pack()

        frameChoice = Frame(frameF)
        frameChoice.pack(side=RIGHT)
        self.Variable = []
        self.v = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        Range = [19, 28, 3, 29-19, 62-28, 9-3, 33-29, 66-62, 11-9]
        for i in range(9):
            scale = Scale(frameChoice, variable=IntVar(), from_=1, to=Range[i], orient=HORIZONTAL)
            scale.pack(anchor=CENTER)
            self.Variable.append(scale)

        Label(self.frame).pack()

        btn = Button(self.frame, text="OK", font=('微软雅黑', 12, "bold"), command=self.print_selection)
        btn.pack()

        self.l = Label(self.frame)
        self.l.pack()

        self.frameModel = Frame(self.frame)
        self.frameModel.pack()
        self.btnL = Button()
        self.btnT = Button()
        self.people = people

    def Learning(self):
        paperBegin(self.v, True, self.people)

    def Testing(self):
        paperBegin(self.v, False, self.people)

    def print_selection(self):
        self.v = [x.get() for x in self.Variable]

        if self.v[0] + self.v[1] + self.v[2] < 20 or self.v[3] + self.v[4] + self.v[5] < 20 or self.v[6] + self.v[7] + \
                self.v[8] < 5:
            self.l.config(text='you have selected less than required level', font=('微软雅黑', 11, "bold"), fg="yellow")
            self.btnL.destroy()
            self.btnT.destroy()
            self.Win.mainloop()
        else:
            self.l.config(text='')
            self.btnL = Button(self.frameModel, text="学习模式", font=('微软雅黑', 12), command=self.Learning)
            self.btnT = Button(self.frameModel, text="考试模式", font=('微软雅黑', 12), command=self.Testing)
            self.btnL.pack(side=LEFT)
            self.btnT.pack(side=RIGHT)
            self.Win.mainloop()


class Register(MyTk):
    def __init__(self):
        super().__init__()

        label = Label(self.frame, text='为Q&A platform for Python注册一个账号',
                      font=('微软雅黑', 16, "bold"))
        label.pack()

        label1 = Label(self.frame, text="请输入注册手机号",
                       font=('微软雅黑', 12))
        label1.pack()
        self.user_phoneNumber = Entry(self.frame)
        self.user_phoneNumber.pack()

        label2 = Label(self.frame, text="请设置密码(不少于6位)",
                       font=('微软雅黑', 12))
        label2.pack()
        self.user_code = Entry(self.frame, show='*')
        self.user_code.pack()

        label3 = Label(self.frame, text="请设置用户名（2-10位)",
                       font=('微软雅黑', 12))
        label3.pack()
        self.user_name = Entry(self.frame)
        self.user_name.pack()

        self.registerButton = Button(self.frame, text='注册', command=self.createLogin,
                                     font=('微软雅黑', 12))
        self.registerButton.pack()

        self.Win.mainloop()

    def createLogin(self):
        phoneNumber = self.user_phoneNumber.get() or ' '
        if phoneNumber.isdigit():
            file = "D:\pyHomework/topInformation.txt"
            with open(file) as fp:
                for line in fp:
                    if (line.split(" "))[0] == phoneNumber:
                        messagebox.showinfo('注册提示', '您好, 该账号已被注册')
                        return
            code = self.user_code.get() or " "
            if code == ' ' or len(code) < 6:
                messagebox.showinfo('注册提示', '您好, 请输入有效密码')
            else:
                name = self.user_name.get() or " "
                if not 10 > len(name) > 1:
                    messagebox.showinfo('注册提示', '您好, 请输入有效名字')
                else:
                    file = "D:\pyHomework/topInformation.txt"
                    fp = open(file, "a")
                    fp.write(
                        self.user_phoneNumber.get() + " " + self.user_code.get() + " " + self.user_name.get() + "\n")
                    messagebox.showinfo('注册提示', self.user_name.get() + '您好,注册成功！')
                    fp.close()
        else:
            messagebox.showinfo('注册提示', '您好, 请用有效手机号码注册一个账号')


class LoginSuccess(MyTk):
    def __init__(self, name, people):
        super().__init__()
        self.x = people
        Label(self.frame, text=name + " 登录成功!\n", font=("微软雅黑", 12, "bold")).pack()
        Button(self.frame, text="题库正确率", font=("微软雅黑", 12), command=self.correctness).pack()
        Button(self.frame, command=self.paper, text="做题", font=("微软雅黑", 12)).pack()
        Button(self.frame, text="个人历史成绩", font=("微软雅黑", 12), command=self.grade).pack()

        self.Win.mainloop()

# ------个人历史成绩查询----------------------------------------
    def grade(self):
        plt.close()
        file = "D:\pyHomework/topInformation.txt"
        grades = []
        with open(file) as fp:
            for line in fp:
                if self.x == line.split(" ")[0]:
                    grades = [int(i) for i in line.split(" ")[3:]]
                    break
        if len(grades) == 0:
            messagebox.showinfo("查询提示", "您当前还没有 试卷模式 做题历史")
        else:
            n = range(1,len(grades)+1)
            plt.plot(n,grades)
            plt.show()

# ------题库准确率查询-------------------------------------------
    def correctness(self):
        frame = MyTk().frame
        Label(frame, text="choose type", font=("微软雅黑", 12, "bold"))
        Button(frame, text="single choice", font=("微软雅黑", 12), command=self.singleCorrectness).pack()
        Button(frame, text="true or false", font=("微软雅黑", 12), command=self.trueOrFalseCorrectness).pack()
        Button(frame, text="short answer", font=("微软雅黑", 12), command=self.shortCorrectness).pack()

    def singleCorrectness(self):
        Correctness("single choice")

    def trueOrFalseCorrectness(self):
        Correctness("true or false")

    def shortCorrectness(self):
        Correctness("short answer")

# ------做题--------------------------------
    def paper(self):
        Choose(self.x)


class Correctness:
    def __init__(self, type):
        # 这两行代码解决 plt 中文显示的问题
        plt.close()
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        path = 'D:\pyHomework/MultipleChoiceQuestions(1).json'
        fp = open(path, 'r', encoding='utf-8')
        self.questionInformation = json.load(fp)
        tmp = [self.questionInformation[type][str(i)]["rate"].split("/") for i in
               range(1, len(self.questionInformation[type]))]
        correctnessDiff = [float(x[0]) / (float(x[1]) + 0.0001) for x in tmp]

        print(correctnessDiff)
        plt.bar(range(1, len(self.questionInformation[type])), correctnessDiff, 0.5)
        plt.title('Correctness of ' + type)

        plt.show()



