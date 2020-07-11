from random import randint
import JC

# HOW IT WORKS:

# The Program iterates through the
# 'AllCards' Array and tests you.

# Correctly answered questions are removed
# as you run the program, until none are left.

# It runs until you got full marks, so
# when the 'AllCards' Array is empty.


# Variables and stuff
Intro = True
ShuffledCards = True
FetchCardFile = True

theCard = -1
answerStart = ''

Commands = ["'Done': Finish answering.", "'Commands': See Commands List"]

# Directory/name of data file
cardFile = "Your Cards" + "\Card Data"

# Specify the bullet layout for the cardFile
# The two bullets can't be the same though.
questionBullet = '> '
answerBullet = '- '

if questionBullet == answerBullet:
    JC.FoundError("questionBullet and answerBullet can't be the same.")
    
def ItsA(what, phrase):
    global AllCards
    global questionBullet
    global answerBullet
    
    if what == "Question":
        return phrase[:len(questionBullet)] == questionBullet
    else:
        return phrase[:len(answerBullet)] == answerBullet
    
# The AllCards Array is laid out as
# AllCards[which question][which answer to the question]
AllCards = [[]]

NewCard = []

# You Hard Coded version of 'AllCards' data, here:
if not FetchCardFile:
    
    AllCards = [
                    # Add your topics here like the below examples
                    ["2 + 2",
                     "4"],
                
                    ["Say 'yes' and 'no'",
                     "yes", "no"]
                    
                    ]

# 'FETCH FILE DATA' ALGORITHM:
else:
    # READ DATA FILE:
    
    # An Array, where each item is a line of data,
    # is added as a single item. Hence 'AllCards[0]'
    AllCards[0] = JC.TryToRead(cardFile).split('\n')
            
    # CLEAN UP DATA LOOPS:
    
    # Remove blank lines/items, == ''
    while '' in AllCards[0]:
        AllCards[0].remove('')

    # Detect Empty Bullet Error.
    if JC.AThingsArrayed([answerBullet, questionBullet], AllCards[0]):
        if answerBullet and questionBullet in AllCards[0]:
            JC.FoundError("Empty question and answer bullets found.")
        elif questionBullet in AllCards[0]:
            JC.FoundError("Empty question bullet(s) found.")
        else:
            JC.FoundError("Empty answer bullet(s) found.")
        
    # DEBULLETING + REORGANISING 'ALLCARDS':
    for item in AllCards[0]:
        if ItsA("Question", item):
            # If a previous question just was now
            # finished, add that previous one first.
            if JC.Any(NewCard):
                AllCards.append(NewCard)
                
                # Reset variables for new question...
                NewCard = []
                theCard += 1
                answerStart = ''
            
            # 'NewCard' is an array/dimension
            # representing a cleaned question and its
            # answers, soon to be added to the 'AllCards'.
            
            # Slice off bullets before adding...
            NewCard.append(item[len(questionBullet):])
        else:
            if JC.Any(NewCard):
                if ItsA("New Answer", item):
                    NewCard.append(item[len(answerBullet):])
                    answerStart = JC.MaxIndex(NewCard)
                else:
                    # Then it must be a continued part of a previous answer, so
                    # add the continuation as part of the original answer part.
                    NewCard[answerStart] += item
            else:
                JC.FoundError("Expected question before answer, got the opposite.")
    
    # Add the last left over 'NewCard'.
    AllCards.append(NewCard)
    del NewCard
    
    # Reduce the first giant array item to
    # include just the first question and its answers.
    del AllCards[0]

    # End of algorithm:

# Lowercase the answers so marking is slightly more lenient.
for question in range(len(AllCards)):
    for answer in range(1, len(AllCards[question])):
        AllCards[question][answer] = AllCards[question][answer].lower()

# The amount of questions before before any deleting.
totalCards = len(AllCards)

# CONSOLE START:
JC.Title(JC.Quote(cardFile[11:]) + " Flash-Carder: (Demo-Only Template)")
JC.AssertDominance()
theCard = -1

if Intro:
    JC.Pace("Before we start:")
    JC.TitledList("Commands List", Commands, False)
    JC.CatchUp()
    print()
    JC.FreshPage()

# ACTUAL PROGRAM LOOP:
while 1:
    
    # SETTING UP:
    ISaidCorrect = False
    
    CorrectAnswers = []
    TheAnswers = []
    UserInputs = []
    
    # Pick Question.
    if ShuffledCards:
        theCard = randint(0, JC.MaxIndex(AllCards))
    else:
        theCard = 0
        
    NewCard = AllCards[theCard]
    
    # Everything apart from the question title
    # (from NewCard[1] upwards) is answers.
    TheAnswers += NewCard[1:]
    
    JC.Spam(">", 2, JC.Delays[0], False)
    
    # ASK QUESTION:
    JC.Pace(' ' + NewCard[0])
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
        # Or accept and save answer.
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
            if yourAnswer.lower() in TheAnswers and yourAnswer not in CorrectAnswers:
                CorrectAnswers.append(yourAnswer)
                
        # OPINION:
        if JC.Any(CorrectAnswers):
            JC.Pace("(I think) you got " + str(len(CorrectAnswers)) +
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
                JC.DramaType("\t- " + yourAnswer + "\t<-\tCorrect!", JC.dramatypeSpeed)
            else:
                JC.DramaType("\t- " + yourAnswer, JC.dramatypeSpeed)
            print()
            JC.Pause(0)
            
        # MARKING FAIL-SAFE:    
        JC.Pause(1)
        ISaidCorrect = JC.OkayWith("\nDid you actually get the question correct?")
    
        # Show remorse...
        if ISaidCorrect: 
            if not len(CorrectAnswers) == len(TheAnswers):
                print("oh, ", end = '')
            if JC.Any(CorrectAnswers):
                JC.SmartPace("Okay then.")
                
    # REMOVE LEARNT QUESTION:
    if ISaidCorrect or len(CorrectAnswers) == len(TheAnswers):
        AllCards.remove(NewCard)
        amountAfterMarking = len(AllCards)
        
        JC.Inform("You have completed " + str(round(100 - (100 * 
            (amountAfterMarking / totalCards)), 1)) + "% of the program")
        JC.CatchUp()
            
    # NEXT OR FINISH:
    if JC.Any(AllCards):
        JC.IsBusy("Next Question")
        JC.FreshPage()
    else:
        JC.FreshPage()
        JC.Pause(1)
        JC.Pace("\nCards Completed: Well Done! end = ''")
        JC.GoAway()
