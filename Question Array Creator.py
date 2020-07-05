import JC
from random import randint

# Modify indents based on how the program's run. 
# For some reason the tabs are very inconsistent 
# cross-platform. Change these as you wish.
PyExeFile = False
PyCharm = True
PyIDLE = False

if PyCharm:
    biggestTab = '\t\t\t\t\t'
elif PyIDLE or PyExeFile:
    biggestTab = '\t\t'
    
    
# All the lambdas help with clarity of the program
Tabify = lambda term: biggestTab + term
Quote = lambda term: '"' + term + '"'

Comma_After = lambda Line: Line + ', '

NewLine_Before = lambda line: '\n' + line
NewLine_After = lambda line: line + '\n'

Start_New_Level = lambda Line: '\n' + biggestTab + Line
Finishing_Bracket = '\n' + biggestTab[1:] + ']'

LastNineChars = lambda string: string[len(string)-9:len(string)]

AddingQuestions = True
Intro = True

def Answer_Num():
    global questionNumber
    global answerNumber
    
    return "Answer " + str(questionNumber) + '.' + str(answerNumber)

def BotTillMax(whichLimit, ifNotFinished):
    global answerNumber
    global botMaxAnswers
    
    global questionNumber
    global botMaxQuestions
    
    if whichLimit == "Questions" and questionNumber - 1 == botMaxQuestions or \
            whichLimit == "Answers" and answerNumber - 1 == botMaxAnswers:
        return "Done"
    else:
        return ifNotFinished

# Starts Here
questionNumber = 0
botMaxQuestions = randint(1, 14)

WholeArray = NewLine_Before("AllQuestions = [")

JC.Title("Question Array Creator: For FlashCards.py")
JC.AssertDominance()

if Intro:
    JC.SmartPace("Creates a string/text version of the 'AllQuestions'")
    JC.SmartPace("Array.")
    
    JC.SmartPace("\nWhen prompted, copy the resulting Array into your")
    JC.SmartPace("version of the FlashCards.py source code end = ''")
    
    JC.Stop()
    print()
    
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
    
    # At first, you must be gettin answers if you
    # adding questions, logically. So this looked nice.
    GettingAnswers = AddingQuestions
    
    # Name it
    QuestionName = JC.SayUntil("Question " + str(questionNumber) +
                               "s Title", "Question " + str(questionNumber))
    WholeArray += Comma_After(Quote(QuestionName))
    WholeArray += Start_New_Level(' ')

    JC.Inform("Type 'Done' when finished adding answers.")
    print()
    
    while GettingAnswers:
        answerNumber += 1
        newAnswer = JC.GetInput(Answer_Num(), BotTillMax("Answers", Answer_Num()))
            
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
    
    # Remove any extra last bits:
    # Comma_After('') + Start_New_Level(' ') is ', \n\t\t\t\t\t '
    if Comma_After('') + Start_New_Level(' ') == LastNineChars(WholeArray):
        # Returns WholeArray without it by slicing it up
        WholeArray = WholeArray[:len(WholeArray)-9]
    if Comma_After('') in LastNineChars(WholeArray):
        WholeArray = WholeArray[:len(WholeArray)-2]
    
    # Close Brackets of the current question
    WholeArray += ']'
    
    JC.Inform("Added Question " + str(questionNumber))
    
    print(WholeArray + Finishing_Bracket)
    JC.Pause(1)
    JC.Inform("Type 'Done' to finish, or anything "
              "\nelse to add another question end = ''")
    
    # Basically if not finished, still add questions
    if not JC.GetInput('', BotTillMax("Questions", "Blahblah")) == "Done":
        # The comma is only added once we know
        # for sure we're still adding questions.
        WholeArray = Comma_After(WholeArray)
    else:
        AddingQuestions = False
        WholeArray += Finishing_Bracket
    print()

JC.SmartPace("Then your finished array is above.")
JC.Pause(2)
JC.SmartPace("\nWhen you're finished copying and")
JC.SmartPace("pasting, type to exit the program.")

JC.GoAway()
