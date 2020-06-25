from JC import A_User, Any
from random import randint
import JC

# The Program iterates through the
# 'AllQuestions' Array and tests you.

# Correctly answered questions are removed
# as you run the program, until none are left.

# It runs until you got full marks, so
# when the 'AllQuestions' Array is empty.

# Variables and stuff

RandomTopics = True
StillAnswering = True

theQuestion = -1
itsName = 0

# tbf this beginning thing is me
# being awkward and 'lazy'
beginning = "Your Question: '"

YourCorrectOnes = []
UserInputs = []
TheAnswers = []

# AllQuestions[which question][which answer to the question]
AllQuestions = [
              # Add your topics here like the below examples
              # (delete them when you understand)...
            
                ["2 + 2",
                 "4"],
            
                ["Say yes and no",
                 "yes", "no"],
            ]

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
        if Any(UserInputs):
            JC.TitledList("Answers Submitted", UserInputs, False)
            JC.Pause(0)
        else:
            print()
            
        # Then input more Answers.
        JC.Pause(2)
        if A_User:
            if not Any(UserInputs):
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
    if not Any(UserInputs):
        JC.Pace("I can't mark that mate!")
    else:
        if Any(YourCorrectOnes):
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

    iSaidCorrect = JC.OkayWithMessage("\nDo you think you got the question "
                                      "correct?")

    JC.SmartPace("\nOkay then.")
    if Any(YourCorrectOnes) or iSaidCorrect:
        if YourCorrectOnes == TheAnswers or iSaidCorrect:
            AllQuestions.remove(thisQuestion)
            amountAfterMarking = len(AllQuestions)
    
        percentage = str(round(100 - (100 * (amountAfterMarking /
                                             Total_Questions)), 2))
        JC.Inform("\nSo far you have completed " + percentage + "% of the "
                                                                "program\n")

    if Any(AllQuestions):
        # Update...
        JC.CatchUp()
        beginning = "Your New Question: '"
        JC.IsBusy("Switching Question")
    else:
        JC.Pace("\nYou've revised everything: - Well Done! ")
        JC.GoAwayIn(2, 4)
