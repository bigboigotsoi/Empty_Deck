import JC
from random import randint


# BRIEF:

# The Program iterates through the
# 'AllQuestions' Array and tests you.

# Correctly answered questions are removed
# as you run the program, until none are left.

# It runs until you got full marks, so
# when the 'AllQuestions' Array is empty.


# Variables and stuff
RandomTopics = True
StillAnswering = True
FetchingDataFile = True

theQuestion = -1
itsName = 0
questionIndex = -1
endOfQuestionOne = 0

# This beginning thing is me
# being awkward and 'lazy'
beginning = "Your Question: '"

# Directory/name of data
dataFile = "Card Data"

# Bullet layout for the dataFile
questionBullet = '>' + ' '
answerBullet = '-' + ' '

YourCorrectOnes = []
AllQuestions = [[]]
NewQuestion = []
UserInputs = []
TheAnswers = []

def ItsA(what, phrase):
    global AllQuestions
    global questionBullet
    global answerBullet
    
    if what == "Question":
        return phrase[:len(questionBullet)] == questionBullet
    else:
        return phrase[:len(answerBullet)] == answerBullet

def NextItem(Array, currentItem):
    try:
        return Array[Array.index(currentItem) + 1]
    except IndexError:
        return ''
    
# The AllQuestions Array is laid out as...
# AllQuestions[which question][which answer to the question]

# Hard Coded copy of 'AllQuestions' data:
if not FetchingDataFile:
    
    AllQuestions = [
                  # Add your topics here like the below examples
                  # (delete them when you understand)...
                
                    ["2 + 2",
                     "4"],
                
                    ["Say yes and no",
                     "yes", "no"],
                ]

# The 'Fetch File Data' Algorithm:
else:
    
    # Splits the 'dataFile' into a single,  one dimensional
    # array, where each item is a line of data from it.
    
    # It's one massive array at first, as a single item. Hence 'AllQuestions[0]'
    AllQuestions[0] = open(dataFile, 'r').read().split('\n')
    
    # Remove blank lines/items, ''
    while '' in AllQuestions[0]:
        AllQuestions[0].remove('')

    for item in AllQuestions[0]:
        if ItsA("Question", item):
            questionIndex += 1
            
            # Start splitting the array, so making
            # new questions from the 2nd question onwards.
            if questionIndex >= 1:
                questionTitle = item
                
                if questionIndex == 1:
                    endOfQuestionOne = AllQuestions[0].index(questionTitle)
                
                # 'NewQuestion' is an array/dimension, which will be added to
                # the 2D 'AllQuestions' Array later
                NewQuestion.append(questionTitle)
                
                # Add Answers to 'NewQuestion' Array
                while ItsA("Answer", NextItem(AllQuestions[0], item)):
                    NewQuestion.append(NextItem(AllQuestions[0], item))
                    item = NextItem(AllQuestions[0], item)
                
                # Add the 'NewQuestion'
                AllQuestions.insert(questionIndex, NewQuestion)
                NewQuestion = []
    
    # The First giant array item is now split up, so now reduce
    # it to include just the first question and its answers.
    del AllQuestions[0][endOfQuestionOne:]
    del NewQuestion

    # Remove all the bullets, by slicing the items up.
    for question in AllQuestions:
        for item in question:
            if ItsA("Question", item):
                question[question.index(item)] = item[len(questionBullet):]
            else:
                question[question.index(item)] = item[len(answerBullet):]
        
    # End of algorithm!
    
    
# Lowercase the answers so it's easier to check them
for question in AllQuestions:
    answerIndex = 1
    while not answerIndex == len(question):
        question[answerIndex] = question[answerIndex].lower()
        answerIndex += 1

# The amount of questions before running
# the program, so before any deleting.
Total_Questions = len(AllQuestions)

# These two detect if a question has been
# completed and deleted from AllQuestions[][].
amountBeforeMarking = len(AllQuestions)
amountAfterMarking = len(AllQuestions)

JC.Title("'Empty' FlashCards: (Read-Only Template)")

JC.AssertDominance()

while 1:
    amountBeforeMarking = len(AllQuestions)
    
    YourCorrectOnes = []
    TheAnswers = []
    UserInputs = []
    
    whichOne = 0
    
    # Pick Question
    if RandomTopics:
        theQuestion = randint(0, len(AllQuestions)-1)
    else:
        theQuestion += 1

    # The entire Question Item from AllQuestions[][].
    # So includes the answers and the actual question 'name'
    thisQuestion = AllQuestions[theQuestion]
    
    # Everything apart from 'name' (from
    # thisQuestion[1] upwards) is answers.
    TheAnswers += thisQuestion
    TheAnswers.remove(thisQuestion[itsName])

    # The 'name' of the question is always the first part
    # of the question info in AllQuestions[theQuestion]
    # thisQuestion[itsName] == thisQuestion[0].
    JC.SmartPace(beginning + thisQuestion[itsName] + "'.\n(Type '0' to "
                                                            "finish answering.)")
    StillAnswering = True
    
    while StillAnswering:
        
        # Show what's already been inputted. 
        if JC.Any(UserInputs):
            JC.TitledList("Answers Submitted", UserInputs, False)
            JC.Pause(0)
        else:
            print()
            
        # Then input more Answers.
        JC.Pause(2)
        if JC.A_User:
            if not JC.Any(UserInputs):
                response = input("Your answer" + JC.cursor)
            else:
                response = input("Your next answer" + JC.cursor)
            if JC.Validate(response, '0'):
                StillAnswering = False
            else:
                UserInputs.append(response)
        else:
            if len(UserInputs) == len(TheAnswers):
                response = JC.GetInput("Your answer", '0')
                StillAnswering = False
            else:
                response = JC.GetInput("Your answer", TheAnswers[whichOne])
                UserInputs.append(response)
                whichOne += 1

    JC.Pause(1)
    JC.IsBusy("Marking Answers")
    
    for yourAnswer in UserInputs:
        if yourAnswer.lower() in TheAnswers and yourAnswer not in YourCorrectOnes:
            YourCorrectOnes.append(yourAnswer)    
        
    # Show Marks
    if not JC.Any(UserInputs):
        JC.Pace("I can't mark that mate!")
    else:
        if JC.Any(YourCorrectOnes):
            JC.SmartPace("(I think) you got " + str(len(YourCorrectOnes)) +
                         "/" + str(len(TheAnswers)) + " correct!")
        else:
            JC.Pace("I think you got them all wrong!?")
    
        # Return some feedback
        JC.Pause(1)
        JC.TitledList("The Answers were", TheAnswers, False)
    
        JC.Pace("\t (Your Entries were:) ")
        JC.Pause(2)
        
        for yourAnswer in UserInputs:
            if yourAnswer.lower() in TheAnswers:
                JC.SmartPace("\t- " + yourAnswer + "\t<-\tCorrect!")
            else:
                JC.SmartPace("\t- " + yourAnswer)

    iSaidCorrect = JC.OkayWith("\nDo you think you got the question correct?")

    JC.SmartPace("\nOkay then.")
    if JC.Any(YourCorrectOnes) or iSaidCorrect:
        if YourCorrectOnes == TheAnswers or iSaidCorrect:
            AllQuestions.remove(thisQuestion)
            amountAfterMarking = len(AllQuestions)
    
        percentage = str(round(100 - (100 * (amountAfterMarking /
                                             Total_Questions)), 2))
        JC.Inform("So far you have completed " + percentage + "% of the program")

    if JC.Any(AllQuestions):
        # Update...
        JC.CatchUp()
        beginning = "Your New Question: '"
        JC.IsBusy("Switching Question")
    else:
        JC.Pace("\nYou've revised everything: - Well Done! ")
        JC.GoAwayIn(2, 4)
