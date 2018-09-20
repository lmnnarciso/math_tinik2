import random
import time
import math
import re

class User(object):
    def __init__(self, userName, score, error, time):
        self.userName = userName
        self.score = score
        self.error = error
        self.time = time
    
    def correct(self):
        self.score += 1
        print("CORRECT!!!")
        
    def wrong(self):
        self.error += 1
        print("WRONG!!!")

    def questionFormat(self, firstNumber, secondNumber, operation):
        print("What is %s %s %s ?")%(firstNumber, operation, secondNumber)

    def answerCheck(self, userAnswer, correctAnswer):
        if(userAnswer == correctAnswer):
            self.correct()
        else:
            self.wrong()
            
    def recordFormat(self):
        recordString = "Player: %s \t - \t Time: %s \t - \t Score: %s \t - \t Errors: %s \n" % (self.userName, self.timeFormat(), self.score, self.error)
        return recordString
    
    def additionQuestion(self):
        firstNumber = random.randint(10, 99)
        secondNumber = random.randint(10, 99)
        questionAnswer = firstNumber + secondNumber
        self.questionFormat(firstNumber, secondNumber, "+")
        print(questionAnswer) #comment out for testing
        userAnswer = input("Enter answer: ")
        self.answerCheck(userAnswer, questionAnswer)

    def subtractionQuestion(self):
        firstNumber = random.randint(10, 99)
        secondNumber = random.randint(10, 99)
        questionAnswer = 0
        if(firstNumber > secondNumber):
            questionAnswer = firstNumber - secondNumber
            self.questionFormat(firstNumber, secondNumber, "-")
        else:
            questionAnswer = secondNumber - firstNumber
            self.questionFormat(secondNumber, firstNumber, "-")
        print(questionAnswer) #comment out for testing
        userAnswer = input("Enter answer: ")
        self.answerCheck(userAnswer, questionAnswer)

    def multiplicationQuestion(self):
        firstNumber = random.randint(10, 99)
        secondNumber = random.choice([i for i in range(0, 10) if i not in [0,1]])
        questionAnswer = firstNumber * secondNumber
        self.questionFormat(firstNumber, secondNumber, "x")
        print(questionAnswer) #comment out for testing
        userAnswer = input("Enter answer: ")
        self.answerCheck(userAnswer, questionAnswer)

    def divisionQuestion(self):
        firstNumber = random.randint(100, 999)
        secondNumber = random.choice([i for i in range(0, 10) if i not in [0,1]])
        excludeList = [0, 1]
        try:
            while(firstNumber%secondNumber > 0):
                excludeList.append(secondNumber)
                secondNumber = random.choice([i for i in range(0, 10) if i not in excludeList])
        except IndexError:
            pass
        if(len(excludeList) == 10):
            secondNumber = 1
        questionAnswer = firstNumber / secondNumber
        self.questionFormat(firstNumber, secondNumber, "/")
        print(questionAnswer) #comment out for testing
        userAnswer = input("Enter answer: ")
        self.answerCheck(userAnswer, questionAnswer)

    #To convert the self.time(seconds) into string version mm:ss
    def timeFormat(self):
        minutes = int(math.floor(self.time/60))
        seconds = int(self.time%60)
        minuteStr = str(minutes)
        secondStr = str(seconds)
        
        if(len(secondStr) == 2):
            pass
        else:
            secondStr = "0" + secondStr

        if(len(minuteStr) == 2):
            pass
        else:
            minuteStr = "0" + minuteStr
            
        return (minuteStr + ":" + secondStr)

    #To convert the mm:ss time format into seconds(integer)
    def timeStrToInt(self, stringTime):
        minutes, seconds = self.timeFormat().split(":")
        toSeconds = int(minutes)*60 + int(seconds)

        return toSeconds

    #To add a new line of record in the 'scoreboard.txt'
    def record(self):
        f = open("scoreboard.txt", "a+")
        f.write("Player: %s \t - \t Time: %s \t - \t Score: %s \t - \t Errors: %s \n" %(self.userName, self.timeFormat(), self.score, self.error))
        
    #To display 'scoreboard.txt'
    def showRecord(self):
        f = open("scoreboard.txt", "r+")
        for num, line in enumerate(f):
            print(str(num+1) + ":\t" + line)

    #To get the mm:ss in the text form so it can be used to sort it       
    def timeExtract(self):
        f = open("scoreboard.txt", "r+")
        nList = list()
        for line in f:
            newLine = "".join(line)
            start = newLine.find("Time:") + 5
            end = start+6
            nList.append(newLine[start:end].strip(' '))
        return nList

    #Function get all mm:ss in the text file and convert it to seconds then save it into a list so it can be use in sorting
    def convertAllTime(self, timeList):
        #print(timeList)
        secondsList = list() 
        for time in timeList:
            print(time)
            minutes, seconds = time.split(":")
            secondsList.append(int(minutes*60)+int(seconds))
        return secondsList

    def updatedSort(self):
        f = open("scoreboard.txt", "r")
        newDict = dict()
        timeList = self.timeExtract()
        secondsList = self.convertAllTime(timeList)
        usernamesList = self.extractUsernames()
        
        for i,line in enumerate(f):
            newDict[line] = secondsList[i]
            
        sortedList = sorted(newDict, key=newDict.get)

        return sortedList
    
    #Uses the convertAllTime function to get all the time(seconds) then use it as a key for sorting the scoreboard.txt
    def sortScoreBoard(self):
        f = open("scoreboard.txt", "r")
        timeList = self.timeExtract()
        secondsList = self.convertAllTime(timeList)
        usernamesList = self.extractUsernames()
            
        sortedList = self.updatedSort()

        #print(sortedList[3])
        #print(secondsList)
        #print(self.time)
        for i, user in enumerate(usernamesList):
            if(self.userName == user):
                if(int(self.time) < int(secondsList[i])):
                    #print("entering" + self.timeFormat())
                    sortedList[i] = self.recordFormat()
                    f = open("scoreboard.txt", "w")
                    for line in sortedList:
                        f.write(line)
            elif(self.userName not in usernamesList):
                #print("entering else")
                self.record()
                
        sortedList = self.updatedSort()
        
        f = open("scoreboard.txt", "w")
        for line in sortedList:
            f.write(line)
        
    #To extract all the usernames the scoreboard.txt
    def extractUsernames(self):
        f = open("scoreboard.txt", "r")
        userList = list()
        for line in f:
            newLine = "".join(line)
            user = re.search(r'Player:(.*?) \t -', newLine).group(1).strip(' ')
            userList.append(user)
        return userList

    def checkIfExist(self):
        f = open("scoreboard.txt", "r")
        newList = dict()
        userList = self.extractUsernames()
        for i, line in enumerate(f):
            newList[line] = userList[i]
        
    #def updateScores(self):
    #    f = open("scoreboard.txt", "rw")
    #    newDict = dict()
    #    timeList = self.timeExtract()
    #    allTimeList = self.convertAllTime(timeList)
    #    usernamesList = self.extractUsernames()
    #    userTime = zip(usernamesList, allTimeList)
                
    
    def questionnaire(self):
        while(True):
            self.userName = raw_input("Username:")
            if(self.userName == ''):
                break
            self.score = 0
            self.error = 0
            self.time = 0
            startTime = time.time()
            while(self.score < 10 and self.error < 10):
                operation = random.randint(0,3)
                if(operation == 0):
                    self.additionQuestion()
                elif(operation == 1):
                    self.subtractionQuestion()
                elif(operation == 2):
                    self.multiplicationQuestion()
                elif(operation == 3):
                    self.divisionQuestion()
            endTime = time.time() - startTime
            self.time = endTime
            if(self.score == 10):
                self.sortScoreBoard()
            
        self.showRecord()
        
user = User("", 0, 0, 0)

user.questionnaire()
