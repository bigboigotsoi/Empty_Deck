import JC
from random import randint
from JC import Aim_Bot, A_User

# Modify indents based on how the
# program's run. For some reason the
# tabs are very inconsistent cross-platform

PyExeFile = False
PyCharm = True
PyIDLE = False

if PyCharm:
    biggestTab = '\t\t\t\t\t'
elif PyIDLE or PyExeFile:
    biggestTab = '\t\t'

Tabify = lambda term: biggestTab + term
Quote = lambda term: '"' + term + '"'

Comma_After = lambda Line: Line + ', '

NewLine_Before = lambda line: '\n' + line
NewLine_After = lambda line: line + '\n'

Start_New_Level = lambda Line: '\n' + biggestTab + Line
Finishing_Bracket = '\n' + biggestTab[1:] + ']'

Answer_Num = lambda qNum, aNum: "Answer " + str(qNum) + '.' + str(aNum)
LastNineChars = lambda string: string[len(string)-9:len(string)]

AddingQuestions = True
Intro = True

def BotTillLimit(whichLimit, ifNotFinished):
    global answerNumber
    global botMaxAnswers
    
    global questionNumber
    global botMaxQuestions
    
    if whichLimit == "Questions" and questionNumber - 1 == botMaxQuestions or \
            whichLimit == "Answers" and answerNumber - 1 == botMaxAnswers:
        return "Done"
    else:
        return ifNotFinished

# PROGRAM START
questionNumber = 0
botMaxQuestions = randint(1, 14)

WholeArray = NewLine_Before("AllQuestions = [")

JC.AssertDominance()

JC.Title("Question Array Creator: For FlashCards.py")

if Intro:
    JC.SmartPace("\nCreates a string/text version of the 'AllQuestions'")
    JC.SmartPace("Array.")
    
    JC.SmartPace("\nWhen prompted, copy the resulting Array into your")
    JC.SmartPace("version of the FlashCards.py source code.")
    JC.Stop()

while AddingQuestions:
    
    # Newlines between questions, 
    # but not the first one
    if not questionNumber == 0:
        WholeArray += NewLine_Before('')
    WholeArray += Start_New_Level('[')
    
    questionNumber += 1
    
    botMaxAnswers = randint(1, 14)
    answerNumber = 0
    theAnswers = ''
    line = ''
    newLevels = 0
    
    GettingAnswers = AddingQuestions
    
    JC.IsBusy("Creating Question " + str(questionNumber))
    
    # Name it
    QuestionName = JC.SayUntil("Question " + str(questionNumber) +
                               "s Title", "Question " + str(questionNumber))
    WholeArray += Comma_After(Quote(QuestionName))
    
    WholeArray += Start_New_Level(' ')
    
    while GettingAnswers:
        answerNumber += 1
        newAnswer = JC.GetInput(Answer_Num(questionNumber, answerNumber),
                                BotTillLimit("Answers",
                                                Answer_Num(questionNumber, answerNumber)))
        
        if not newAnswer.lower() == "done":
            # Add it
            theAnswers += Comma_After(Quote(newAnswer))
            line += Comma_After(Quote(newAnswer))
            
            # If the Line's too long, add
            # newLine to wrap the array a bit.
            if len(line) > 40:
                theAnswers += Start_New_Level(' ')
                line = ''
        else:
            GettingAnswers = False
    
    WholeArray += theAnswers
    
    # Remove any extra last bits
    # Comma_After(Start_New_Level(WholeArray) is ', \n\t\t\t\t\t'
    if Comma_After('') + Start_New_Level(' ') == LastNineChars(WholeArray):
        # Returns WholeArray without it
        WholeArray = WholeArray[:len(WholeArray)-9]
    if Comma_After('') in LastNineChars(WholeArray):
        WholeArray = WholeArray[:len(WholeArray)-2]
    
    # Close Brackets of the current question
    WholeArray += ']'
    
    JC.Inform("Added Question " + str(questionNumber))
    print(WholeArray + Finishing_Bracket)
    JC.Pause(1)
    
    # Basically if not finished, still adding questions
    if not JC.GetInput("\nType 'Done' to finish, or anything \n"
                       "else to add another question" + JC.cursor,
                              BotTillLimit("Questions", "Blahblah")) == "Done":
        # The comma is only added once we know
        # for sure we're still adding questions.
        WholeArray = Comma_After(WholeArray)
    else:
        AddingQuestions = False
        WholeArray += Finishing_Bracket

JC.SmartPace("\nThen your finished array is above.")
JC.Pause(2)
JC.SmartPace("\nWhen you're finished copying and")
JC.SmartPace("pasting, type to exit the program.")

JC.GoAway()
