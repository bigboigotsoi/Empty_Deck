from random import randint
import JC, os

# HOW IT WORKS:

# The Carder iterates through the
# 'AllCards' Array and tests you.

# Correctly answered questions are removed
# as you run the program, until none are left.

# It runs until you got full marks, so
# when the 'AllCards' Array is empty.

# JC.Release_Ready()

# Variables and stuff
Intro = True
ShuffledCards = True

theCard = -1
answerStart = ''

def ItsA(what, phrase):
    global AllCards
    global questionBullet
    global answerBullet
    
    if what == "Question":
        return phrase[:len(questionBullet)] == questionBullet
    else:
        return phrase[:len(answerBullet)] == answerBullet

Commands = ["'Enter': Finish answering.", "'Commands': See Commands List"]

# Directory/name of the DEFAULT data file.
cardFolder = "Your Cards\\"
cardFile = "Card Data"

# Bullet layout for the cardFile,
# but the two can't be the same though.
questionBullet = '> '
answerBullet = '- '

if questionBullet == answerBullet:
    JC.FoundError("questionBullet and answerBullet can't be the same.")

# DEFAULT CARD FILE START:
JC.Title(" Flash-Carder: ")

JC.IsBusy("Loading default card file: " + JC.Quote(cardFile), False)

# 'YOUR CARDS' FILE EXPLORER:
if len(os.listdir(cardFolder)) > 1:
    if JC.OkayWith("\nWould you like to choose a different file?"):
        theCard += 1
        AllCards = []
        JC.Pace('\n' + JC.Quote(cardFolder) + " Card Folder:")
        
        # Build a kind of file tree thing...
        for file in os.listdir(cardFolder):
            # Draw...
            print(' |')
            theCard += 1
            AllCards.append('(' + str(theCard) + ')--> ' + file)
            
            # Add file to the tree...
            JC.DramaType(AllCards[JC.MaxIndex(AllCards)], 1)
            print()
        print()
        
        theCard = int(input("Which file number would you like to load?" + JC.cursor))
        
        JC.RangeCheck(1, theCard, len(AllCards))
        
        # Cut off the extra tree part to get the card file name...
        cardFile = AllCards[int(theCard) - 1][JC.Digits(theCard) + 6:]
        theCard = -1
        print()
        
        JC.IsBusy("Loading new card file: " + JC.Quote(cardFile), False)
    else:
        JC.Pace("\nOkay then  end = ''")
        JC.IsBusy("Resuming loading " + JC.Quote(cardFile), False)
    
cardFile = cardFolder + cardFile
JC.FreshPage()

# The AllCards Array is laid out as
# AllCards[which question][which answer to the question]
AllCards = [[]]

NewCard = []

# 'FETCH FILE DATA' ALGORITHM:

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
        JC.FoundError("Empty question and/or answer bullets found.")
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

# Reduce the first giant array item to
# include just the first question and its answers.
del AllCards[0]

del NewCard
# End of algorithm:

# Lowercase the answers so marking is slightly more lenient.
for question in range(len(AllCards)):
    for answer in range(1, len(AllCards[question])):
        AllCards[question][answer] = AllCards[question][answer].lower()

# The amount of questions before before any deleting.
totalCards = len(AllCards)

# CUSTOM CARD CHOICE START:
JC.Title(JC.Quote(cardFile[cardFile.index('\ '[0]) + 1:]) + " Flash-Carder:")

JC.AssertDominance()
JC.Pace("(There are " + str(totalCards) + " questions)")
theCard = -1

if Intro:
    JC.TitledList("Commands List", Commands, False)
    JC.CatchUp()
    JC.FreshPage()

JC.IsBusy("Starting", True)

# CARD FLASHING LOOP:
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
    
    if len(TheAnswers) > 1:
        JC.Pace("* There are " + str(len(TheAnswers))
                  + " answers/parts to this question. *\n")
        
    JC.Spam(">", 2, JC.Delays[0], False)

    # ASK QUESTION:
    JC.Pace(' ' + NewCard[0])
    print()
    
    StillAnswering = True
    whichOne = -1
    
    # GET ANSWERS:
    while StillAnswering:
        whichOne += 1
        response = JC.GetInput("Your answer", JC.BotSlowIterate(TheAnswers, ''))
        
        # Detect Commands.
        if response.lower() == 'remind':
            JC.TitledList("Answers Submitted", UserInputs, False)
            JC.Pause(0)
        elif response.lower() == 'commands':
            JC.TitledList("Commands List", Commands, False)
            JC.Pause(0)
        elif response.lower() == '':
            if JC.Any(UserInputs):
                StillAnswering = False
            else:
                JC.Pace("Gotta give an answer first mate!")
                print()
                
        # Or accept and save answer.
        else:
            UserInputs.append(response)
    
    # MARKING:
    JC.Pause(0)
    JC.FreshPage()
    JC.IsBusy("Marking Answers", True)
    
    for yourAnswer in UserInputs:
        if yourAnswer.lower() in TheAnswers and yourAnswer not in CorrectAnswers:
            CorrectAnswers.append(yourAnswer)
    
    # FEEDBACK:
    print('\t' + JC.listStart + "The answers were:" + JC.listEnd)
    JC.List(TheAnswers, False)
    
    print('\t' + JC.listStart + "Your entries were:" + JC.listEnd)
    JC.Pause(1)
    
    for yourAnswer in UserInputs:
        if yourAnswer.lower() in TheAnswers:
            JC.DramaType("\t- " + yourAnswer + "\t<- Correct!", JC.dramatypeSpeed)
        else:
            JC.DramaType("\t- " + yourAnswer, JC.dramatypeSpeed)
        print()
        JC.Pause(0)
        
    # MARKING FAIL-SAFE:
    JC.Pause(1)
    ISaidCorrect = JC.OkayWith("\nDid you get the question correct?")

    # Be suprised perhaps...
    if ISaidCorrect:
        if not len(CorrectAnswers) == len(TheAnswers):
            print("oh...")
        if JC.Any(CorrectAnswers):
            JC.SmartPace("Okay then.")
                
    # REMOVE LEARNT QUESTION:
    if ISaidCorrect or len(CorrectAnswers) == len(TheAnswers):
        AllCards.remove(NewCard)
        amountAfterMarking = len(AllCards)
        
        JC.Inform("You have completed " + str(round(100 - (100 * 
            (amountAfterMarking / totalCards)), 1)) + "% of the program")
        
            
    # NEXT OR FINISH:
    if JC.Any(AllCards):
        JC.CatchUp()
        JC.IsBusy("Next Question", True)
        JC.FreshPage()
    else:
        JC.FreshPage()
        JC.Pause(1)
        JC.Pace("\nAll Cards Learnt: Well Done! end = ''")
        JC.GoAway()
