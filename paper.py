import json
from tkinter import *
import random
from tkinter import messagebox
from matplotlib import pyplot

from MyTk import MyTk
from question import SingleQuestion, TrueOrFalseQuestion, ShortAnswerQuestion


class Paper(MyTk):
    def __init__(self, numbers):
        super(Paper, self).__init__()
        sizex = 850
        sizey = 800
        posx = 200
        posy = 10
        self.Win.title("Paper")
        self.Win.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))

        self.frame = Frame(self.Win, relief=GROOVE, width=650, height=800, bd=1)
        self.frame.place(x=10, y=10)

        self.canvas = Canvas(self.frame, width=650, height=400, bg="pink")
        self.frame1 = Frame(self.canvas)
        myscrollbar = Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=myscrollbar.set)
        myscrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((0, 0), window=self.frame1, anchor='nw')
        self.frame1.bind("<Configure>", self.scroll)

        self.count = 1
        self.submitButton = Button(self.frame1, text="ok", command=self.checkTotal)

        path = 'D:\pyHomework/MultipleChoiceQuestions(1).json'
        fp = open(path, 'r', encoding='utf-8')
        self.questionInformation = json.load(fp)

        self.questions = []

        self.chooseQuestion("single choice", numbers[0], numbers[1], numbers[2])
        self.chooseQuestion("true or false", numbers[3], numbers[4], numbers[5])
        self.chooseQuestion("short answer", numbers[6], numbers[7], numbers[8])

    def chooseQuestion(self, questionType, numberEasy, numberNormal, numberHard):
        QuestionEasy = []
        QuestionNormal = []
        QuestionHard = []
        questionRange = self.questionInformation[questionType]
        l = len(questionRange)
        for i in range(l):
            x = questionRange[str(i + 1)]["difficulty"]
            if x == "easy":
                QuestionEasy.append(i + 1)
            elif x == "normal":
                QuestionNormal.append(i + 1)
            else:
                QuestionHard.append(i + 1)
        QuestionKind = random.sample(QuestionEasy, numberEasy) \
                       + random.sample(QuestionNormal, numberNormal) + random.sample(QuestionHard, numberHard)
        for i in QuestionKind:
            if questionType == "single choice":
                self.questions.append(SingleQuestion(i, self.count, self.frame1, self.questionInformation))
            elif questionType == "true or false":
                self.questions.append(TrueOrFalseQuestion(i, self.count, self.frame1, self.questionInformation))
            else:
                self.questions.append(ShortAnswerQuestion(i, self.count, self.frame1, self.questionInformation))
            self.count += 1

    def scroll(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=800, height=600)

    def pieChartCheck(self):
        pyplot.close()
        n = 0
        i = 0.001
        for q in self.questions:
            i += 1
            if not q.check():
                n += 1
        rateFalse = n / i
        pyplot.rcParams['font.sans-serif'] = ['SimHei']
        pyplot.rcParams['axes.unicode_minus'] = False
        pyplot.title("目前练习正确率")
        size = [rateFalse, (1 - rateFalse)]
        labels = ['Error Rate', 'Correctness']
        colors = ["red", "green"]
        explode = (0.03, 0.02)
        pyplot.pie(size, labels=labels, explode=explode, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        pyplot.axis('equal')
        pyplot.show()

    def learningMode(self):
        Button(self.frame, text="check", command=self.pieChartCheck).place(x=10, y=10)
        for x in self.questions:
            x.pack()
            x.learningMode()

        self.Win.mainloop()

    def testingMode(self):
        for x in self.questions:
            x.pack()
        self.submitButton.pack()

        self.Win.mainloop()

    def checkTotal(self):
        n = 0
        wrongQ = []
        i = 0
        for q in self.questions:
            i += 1
            if q.answerLearningModeSubmit():
                n += 1
            else:
                wrongQ.append(str(i))

        text = "\n\n\n\nyou get " + str(
            int(n / len(self.questions) * 100)) + " points\n\n\nyour wrong points are:\n\n"
        text += " ".join(wrongQ) + "\n\n\n"
        scoreLabel = Label(self.frame1, text=text, bg="pink")
        scoreLabel.pack(fill="x")
        messagebox.showinfo('试卷结果', text)
        self.submitButton.config(state="disable")
        self.Win.mainloop()
