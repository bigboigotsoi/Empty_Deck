import JC, time
from random import randint

# HOW IT WORKS:

# The Program iterates through the
# 'AllQuestions' Array and tests you.

# Correctly answered questions are removed
# as you run the program, until none are left.

# It runs until you got full marks, so
# when the 'AllQuestions' Array is empty.


# Variables and stuff
Intro = True
RandomTopics = True
FetchingDataFile = True

theQuestion = -1
current = -1

Commands = ["'Done': Finish answering.", "'Commands': See Commands List"]

# Directory/name of data file
dataFile = "Card Data"

# Specify the bullet layout for the dataFile
# The two bullets can't be the same though.
questionBullet = '> '
answerBullet = '- '

if questionBullet == answerBullet:
    JC.FoundError("questionBullet and answerBullet can't be the same.")
    
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
    
# The AllQuestions Array is laid out as
# AllQuestions[which question][which answer to the question]
AllQuestions = [[]]

# You Hard Coded version of 'AllQuestions' data, here:
if not FetchingDataFile:
    
    AllQuestions = [
                    # Add your topics here like the below examples
                    ["2 + 2",
                     "4"],
                
                    ["Say 'yes' and 'no'",
                     "yes", "no"]
                    
                    ]

# 'FETCH FILE DATA' ALGORITHM:
else:
    # Splits the 'dataFile' into a single, one 
    # dimensional array, where each item is a line of data from it. 
    
    # Then adds this array as a single item. Hence 'AllQuestions[0]'
    AllQuestions[0] = JC.TryToRead(dataFile).split('\n')
    
    # Remove blank lines/items, ''
    while '' in AllQuestions[0]:
        AllQuestions[0].remove('')
        
    endOfQuestionOne = 0
    for item in AllQuestions[0]:
        if ItsA("Question", item):
            NewQuestion = []
            theQuestion += 1
    
            # Start splitting the array, so making
            # new questions from the 2nd question onwards.
            if theQuestion >= 1:
                # If 2nd Question the 1st one would have just ended...
                if theQuestion == 1:
                    endOfQuestionOne = AllQuestions[0].index(item)
                
                # 'NewQuestion' is an array/dimension, which will
                # be added to the 2D 'AllQuestions' Array later.
                NewQuestion.append(item)
                
                # Add Answers to 'NewQuestion' Array
                while ItsA("Answer", NextItem(AllQuestions[0], item)):
                    NewQuestion.append(NextItem(AllQuestions[0], item))
                    item = NextItem(AllQuestions[0], item)
                
                # Add the finished 'NewQuestion' to 'AllQuestions'
                AllQuestions.insert(theQuestion, NewQuestion)
                del NewQuestion
                
    # The First giant array item is now split up, so now reduce
    # it to include just the first question and its answers.
    del AllQuestions[0][endOfQuestionOne:]
    
    # Remove all the bullets, by slicing the items up.
    for question in AllQuestions:
        for item in question:
            if ItsA("Question", item):
                question[question.index(item)] = item[len(questionBullet):]
            else:
                question[question.index(item)] = item[len(answerBullet):]
        
    # End of algorithm:

# Lowercase the answers so marking is slightly more lenient.
for question in range(len(AllQuestions)):
    for answer in range(1, len(AllQuestions[question])):
        AllQuestions[question][answer] = AllQuestions[question][answer].lower()

# The amount of questions before running
# the program, so before any deleting.
Total_Questions = len(AllQuestions)

# To detect if a question has been
# completed and deleted from AllQuestions[][].
amountAfterMarking = len(AllQuestions)

# CONSOLE START:
JC.Title("'Empty' FlashCards: (Demo-Only Template)")
JC.AssertDominance()
theQuestion = -1

if Intro:
    JC.Pace("Before we start:")
    JC.TitledList("Commands List", Commands, False)
    JC.CatchUp()
    print()
    JC.FreshPage()

# ACTUAL PROGRAM LOOP:
while 1:
    
    # SETTING UP:
    iSaidCorrect = False
    
    YourCorrectOnes = []
    TheAnswers = []
    UserInputs = []
    
    # Pick Question.
    if RandomTopics:
        theQuestion = randint(0, len(AllQuestions)-1)
    else:
        theQuestion = 0
        
    NewQuestion = AllQuestions[theQuestion]
    
    # Everything apart from the question title
    # (from NewQuestion[1] upwards) is answers.
    TheAnswers += NewQuestion[1:]
    
    JC.Spam(">", 2, JC.Delays[0], False)
    
    # ASK QUESTION:
    JC.Pace(' ' + NewQuestion[0])
    print()
    StillAnswering = True
    whichOne = -1
    
    # GET ANSWERS:
    while StillAnswering:
        whichOne += 1
        response = JC.GetInput("Your answer", JC.BotSlowIterate(TheAnswers, "Done"))
        
        # Detect Commands.
        if response.lower() == 'remind':
            JC.TitledList("Answers Submitted", UserInputs, False)
            JC.Pause(0)
        elif response.lower() == 'commands':
            JC.TitledList("Commands List", Commands, False)
            JC.Pause(0)
        elif response.lower() == 'done':
            StillAnswering = False
        # Or accept answer.
        else:
            UserInputs.append(response)
    
    # MARKING:
    JC.Pause(0)
    if not JC.Any(UserInputs):
        JC.Pace("I can't mark that mate!")
    else:
        JC.FreshPage()
        JC.IsBusy("Marking Answers")
        for yourAnswer in UserInputs:
            if yourAnswer.lower() in TheAnswers and yourAnswer not in YourCorrectOnes:
                YourCorrectOnes.append(yourAnswer)
                
        if JC.Any(YourCorrectOnes):
            JC.Pace("(I think) you got " + str(len(YourCorrectOnes)) +
                         "/" + str(len(TheAnswers)) + " correct!")
        else:
            JC.Pace("I think you got them all wrong!?")
        JC.Pause(0)
        
        # FEEDBACK:
        JC.TitledList("The answers were", TheAnswers, False)
    
        print("\t Your entries were: ")
        JC.Pause(1)
        
        for yourAnswer in UserInputs:
            if yourAnswer.lower() in TheAnswers:
                print("\t- " + yourAnswer + "\t<-\tCorrect!")
            else:
                print("\t- " + yourAnswer)
            time.sleep(JC.Delays[0]/2)
    
        JC.Pause(1)
        iSaidCorrect = JC.OkayWith("\nDid you actually get the question correct?")
    
        # If I messed up...
        if iSaidCorrect and not len(YourCorrectOnes) == len(TheAnswers) :
            print("oh, ", end = '')
        
    # PREPARING FOR NEXT QUESTION:
    if JC.Any(YourCorrectOnes) or iSaidCorrect:
        JC.SmartPace("Okay then.")
        
        # Delete complete/learnt question.
        if YourCorrectOnes == TheAnswers or iSaidCorrect:
            AllQuestions.remove(NewQuestion)
            amountAfterMarking = len(AllQuestions)
        
    # NEXT OR FINISH:
    if JC.Any(AllQuestions):
        # Update...
        JC.Inform("You have completed " + str(round(100 - (100 *
                         (amountAfterMarking / Total_Questions)), 2)) + "% of the program")
        JC.CatchUp()
        JC.IsBusy("Next Question")
        JC.FreshPage()
    else:
        # Finish...
        JC.FreshPage()
        JC.Pause(1)
        JC.Pace("\nCards Completed: Well Done! end = ''")
        JC.GoAwayIn(2, False)
