import json
import textwrap
import random
from tkinter import *
from tkinter import messagebox

import scroll as scroll
from matplotlib import pyplot

from MyTk import MyTk

# -----总的试题类型----------------------
class Question(Frame):
    def __init__(self, question_id, sequence_id, root, questionInformation, type):
        super().__init__(root, width=800, height=240)
        self.root = root
        self.propagate(False)
        self.questionId = question_id
        self.sequenceId = sequence_id
        self.label = Label(self)
        self.label.pack()
        labelSequenceId = Label(self, text=str(self.sequenceId), bg='grey')
        labelSequenceId.pack(fill="x")

        self.learningModeButton = Button(self)

        self.questionInformation = questionInformation

        self.path = 'D:\pyHomework/MultipleChoiceQuestions(1).json'
        self.type = type
        print(str(self.questionId))
        text = textwrap.fill(self.questionInformation[type][str(self.questionId)]["question"], 60)
        labelQuestion = Label(self, text=text)
        labelQuestion.pack()

        self.answer = IntVar()
        self.answer.set(0)
        self.intAnswer = 0
        self.buttons = []
        i = 0
        for description in self.questionInformation[type][str(self.questionId)]["choices"]:
            t = textwrap.fill(self.questionInformation[type][str(self.questionId)]["choices"][description], 60)
            buttonAnswers = Radiobutton(self, text=t, variable=self.answer, value=i, command=self.getAnswer)
            buttonAnswers.pack()
            self.buttons.append(buttonAnswers)
            i += 1

    def getAnswer(self):
        self.intAnswer = self.answer.get()
        print(self.intAnswer)
        selection = "You selected the option " + str(self.answer.get())
        self.label.config(text=selection)

    def submit(self, userAnswer, ReferenceAnswer):
        right = (ReferenceAnswer == userAnswer)
        color = "red"
        if right:
            color = "green"
        LabelReferenceAnswer = Label(self,
                                     text="Reference Answer is " + ReferenceAnswer + ", your choice is " + str(right),
                                     bg=color)

        LabelReferenceAnswer.pack()

        return right

    def learningModeSubmit(self, userAnswer, ReferenceAnswer):
        rate = str(self.questionInformation[self.type][str(self.questionId)]["rate"]).split("/")
        right = self.submit(userAnswer, ReferenceAnswer)
        if right:
            rate[0] = str(int(rate[0]) + 1)
        rate[1] = str(int(rate[1]) + 1)
        self.questionInformation[self.type][str(self.questionId)]["rate"] = rate[0] + "/" + rate[1]
        with open(self.path, "w", encoding='utf-8') as jsonFile:
            jsonFile.write(json.dumps(self.questionInformation, ensure_ascii=False))
        return right


class SingleQuestion(Question):
    def __init__(self, question_id, sequence_id, root, questionInformation):
        super().__init__(question_id, sequence_id, root, questionInformation, "single choice")

    def learningMode(self):
        self.learningModeButton = Button(self, text="OK", command=self.answerLearningModeSubmit)
        self.learningModeButton.pack()

    def answerSubmit(self):
        print("t", self.intAnswer)
        userAnswer = chr(self.intAnswer + ord("A"))
        referenceAnswer = chr(int(self.questionInformation["single choice"][str(self.questionId)]["answer"]) + ord("A"))
        return super().submit(userAnswer, referenceAnswer)

    def answerLearningModeSubmit(self):
        print("t", self.intAnswer)
        userAnswer = chr(self.intAnswer + ord("A"))
        referenceAnswer = chr(int(self.questionInformation["single choice"][str(self.questionId)]["answer"]) + ord("A"))
        self.learningModeButton.config(state="disable")
        return super().learningModeSubmit(userAnswer, referenceAnswer)

    def check(self):
        userAnswer = chr(self.intAnswer + ord("A"))
        referenceAnswer = chr(int(self.questionInformation["single choice"][str(self.questionId)]["answer"]) + ord("A"))
        return userAnswer == referenceAnswer


class TrueOrFalseQuestion(Question):
    def __init__(self, question_id, sequence_id, root, questionInformation):
        super().__init__(question_id, sequence_id, root, questionInformation, "true or false")

    def learningMode(self):
        Button(self, text="OK", command=self.answerLearningModeSubmit).pack()

    def answerSubmit(self):
        userAnswer = referenceAnswer = "False"
        if self.intAnswer == 0:
            userAnswer = "True"
        if self.questionInformation["true or false"][str(self.questionId)]["answer"] == "0":
            referenceAnswer = "True"
        return super().submit(userAnswer, referenceAnswer)

    def check(self):
        userAnswer = referenceAnswer = "False"
        if self.intAnswer == 0:
            userAnswer = "True"
        if self.questionInformation["true or false"][str(self.questionId)]["answer"] == "0":
            referenceAnswer = "True"
        return userAnswer == referenceAnswer

    def answerLearningModeSubmit(self):
        userAnswer = referenceAnswer = "False"
        print(self.intAnswer, self.questionInformation["true or false"][str(self.questionId)]["answer"])
        if self.intAnswer == 0:
            userAnswer = "True"
        if self.questionInformation["true or false"][str(self.questionId)]["answer"] == "0":
            referenceAnswer = "True"
        print(userAnswer, referenceAnswer)
        return super().learningModeSubmit(userAnswer, referenceAnswer)


class ShortAnswerQuestion(Question):
    def __init__(self, question_id, sequence_id, root, questionInformation):
        super().__init__(question_id, sequence_id, root, questionInformation, "short answer")
        entry_var = StringVar()
        Entry(self, width=20, textvariable=entry_var).pack()
        entry_var.set('请输入答案')

    def learningMode(self):
        Button(self, text="OK", command=self.answerLearningModeSubmit).pack()

    def answerSubmit(self):
        return True

    def answerLearningModeSubmit(self):
        text = textwrap.fill(
            "Reference Answer: " + self.questionInformation["short answer"][str(self.questionId)]["answer"], 50)
        LabelReferenceAnswer = Label(self,
                                     text=text,
                                     bg="green")

        LabelReferenceAnswer.pack()

    def check(self):
        return True


def setNumbers(n):
    global numbers
    numbers = n


def chooseQuestion(questionType, numberEasy, numberNormal, numberHard, count, questions, questionInformation, frame1):
    QuestionEasy = []
    QuestionNormal = []
    QuestionHard = []
    questionRange = questionInformation[questionType]
    l = len(questionRange)
    for i in range(l):
        x = questionRange[str(i + 1)]["difficulty"]
        if x == "easy":
            QuestionEasy.append(i + 1)
        elif x == "normal":
            QuestionNormal.append(i + 1)
        else:
            QuestionHard.append(i + 1)
    print(QuestionNormal)
    print(numberNormal)
    QuestionKind = random.sample(QuestionEasy, numberEasy) + random.sample(QuestionNormal,
                                                                           numberNormal) + random.sample(QuestionHard,
                                                                                                         numberHard)
    for i in QuestionKind:
        if questionType == "single choice":
            questions.append(SingleQuestion(i, count, frame1, questionInformation))
        elif questionType == "true or false":
            questions.append(TrueOrFalseQuestion(i, count, frame1, questionInformation))
        else:
            questions.append(ShortAnswerQuestion(i, count, frame1, questionInformation))
        count += 1
    return count


def pieChartCheck(questions):
    pyplot.close()
    n = 0
    i = 0.001
    for q in questions:
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


def learningMode(questions, root, p):
    def pieChartCheck1():
        pieChartCheck(questions)

    print("yes!")
    Button(root, text="check", command=pieChartCheck1).place(x=10, y=10)
    for x in questions:
        x.pack()
        x.learningMode()
    print("yes!")
    p.Win.mainloop()


def testingMode(questions, submitButton, p):
    for x in questions:
        x.pack()
    submitButton.pack()
    p.Win.mainloop()


def checkTotal(questions, frame1, p, people, submitButton):
    n = 0
    wrongQ = []
    i = 0
    for q in questions:
        i += 1
        if q.answerLearningModeSubmit():
            n += 1
        else:
            wrongQ.append(str(i))

    text = "\n\n\n\nyou get " + str(
        int(n / len(questions) * 100)) + " points ！\n\n\nyour wrong points are:\n\n"
    text += " ".join(wrongQ) + "\n\n\n"
    text = textwrap.fill(text, 80)

    scoreLabel = Label(frame1, text=text, bg="pink", font=("微软雅黑", 12, "bold"))
    scoreLabel.pack(fill="x")
    messagebox.showinfo('试卷结果', text)
    submitButton.config(state="disable")

    print("d")
    file = "D:\pyHomework/topInformation.txt"
    fp = open(file, 'r')
    info = fp.readlines()
    fp.close()
    for i in range(len(info)):
        line = info[i]
        print(line)
        print((line.split(" "))[0], people)
        if (line.split(" "))[0] == people:
            info[i] = info[i][0:-1] + (" " + str(int(n / len(questions) * 100)) + "\n")
            break

    fp = open(file, 'w')
    fp.writelines(info)
    fp.close()
    p.Win.mainloop()


def paperBegin(numbers, test, people):
    def scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"), width=800, height=600)

    def checkTotal1():
        checkTotal(questions, frame1, p, people, submitButton)

    p = MyTk()
    sizex = 850
    sizey = 800
    posx = 200
    posy = 10
    p.Win.title("Paper")
    p.Win.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))

    p.frame = Frame(p.Win, relief=GROOVE, width=650, height=800, bd=1)
    p.frame.place(x=10, y=10)

    canvas = Canvas(p.frame, width=650, height=400, bg="pink")
    frame1 = Frame(canvas)
    myscrollbar = Scrollbar(p.frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=myscrollbar.set)
    myscrollbar.pack(side="right", fill="y")
    canvas.pack(side="left")
    canvas.create_window((0, 0), window=frame1, anchor='nw')
    frame1.bind("<Configure>", scroll)
    count = 1
    submitButton = Button(frame1, text="ok", command=checkTotal1)

    path = 'D:\pyHomework/MultipleChoiceQuestions(1).json'
    fp = open(path, 'r', encoding='utf-8')
    questionInformation = json.load(fp)
    print(type(questionInformation))
    questions = []
    count = chooseQuestion("single choice", numbers[0], numbers[1], numbers[2], count, questions, questionInformation,
                           frame1)
    count = chooseQuestion("true or false", numbers[3], numbers[4], numbers[5], count, questions, questionInformation,
                           frame1)
    chooseQuestion("short answer", numbers[6], numbers[7], numbers[8], count, questions, questionInformation, frame1)
    if test:
        learningMode(questions, p.frame, p)
    else:
        testingMode(questions, submitButton, p)


'''
t = Tk()
frame = Frame(t)
frame.pack()
canvas = Canvas(frame, width=650, height=400, bg="pink")
frame1 = Frame(canvas)
myscrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=myscrollbar.set)
myscrollbar.pack(side="right", fill="y")
canvas.pack(side="left")
canvas.create_window((0, 0), window=frame1, anchor='nw')
frame1.bind("<Configure>", scroll)
path = 'D:\pyHomework/MultipleChoiceQuestions(1).json'
fp = open(path, 'r', encoding='utf-8')
f=[]
questionInformation = json.load(fp)
for i in range(1,9):
    f1 = SingleQuestion(i, i, frame1, questionInformation)
    f.append(f1)
Button(frame, text="check").place(x=10, y=10)
for x in f:
    x.pack()
    x.learningMode()

t.mainloop()
'''
