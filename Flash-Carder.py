from random import choice as ChooseFrom

import JC
import os

# Carder iterates through the
# 'Deck' Array and tests you.

# Correctly answered questions
# are removed until none are left.

# Runs until full marks, so when 
# the 'Deck' Array is empty.

# VARIABLES/DATA:
Intro = True
Harsh = False
CanExplore = True
ShuffleDecks = True

# Directory + name of the DEFAULT data file.
deckFolder = "Your Decks\\"
deckFile = "Deck Data - 1.txt"

questionBullet = '> '
answerBullet = '- '
commentBullet = '# '

checkpoint = 3

Remarks = [
        # Correct answer remarks...
        ["Yep", "Correctumundo", "Mate, spot on", "You're decent at this",
         "Wowee Correct", "Correct", "Obviously, correct", "Alright mate",
         "There's no fooling you", "I'll give you that", "Bang on",
         "Pretty much", "Perfect", "Good choice", "You remembered that one"],
        
        # Remarks for new streaks...
        ["That's crazy", "Now that's impressive", "Take care of it",
         "Don't lose it", "Thats pretty big", "At least it's not " +
         ChooseFrom(["zero", "nothing"]) + "Better than " +
         ChooseFrom(["zero", "nothing"]) + " I guess", "Look after it okay",
         "Keep it safe", "That's unreal", "Didn't think you'd get this far",
         "I'm actually suprised", "Wasn't expecting that", "You cheated",
         "You'll lose it soon anyway", "Bet it won't last though"],
        
        # Remarks for new streaks and correct answers....
        ["Great", "Keep it up", "Nice one", "Nicely Done", "Get in there mate",
         "Keep it up", "Hey... that's pretty good", '', "Lets gooo",
         "You're getting good at this", "EZ", "ez", "gg ez", "2 ez",
         "Easy", "Thats half-decent", "You're on it today", "Looking good"]]

Commands = ["'Enter'     :>  Finish answering.",
            "'Commands'  :>  See Commands List"]

AnswerWords = []

# Carder-Unique Functions...

def FixSpaces(phrase):
    while '  ' in phrase:
        phrase = phrase.replace('  ', ' ')

    while '\t' in phrase:
        phrase = phrase.replace('\t', ' ')

    while '\n' in phrase:
        phrase = phrase.replace('\n', ' ')

    return phrase

def ItsA(what, phrase):
    global Deck
    global questionBullet
    global answerBullet
    
    # Finds out by checking the bullet region/slice of the phrase.
    if "question" in JC.Pure(what):
        bullet = questionBullet
        return phrase[:len(questionBullet)] == questionBullet
    elif "answer" in JC.Pure(what):
        return phrase[:len(answerBullet)] == answerBullet
    else:
        return phrase[:len(commentBullet)] == commentBullet    

def Crowd(Banner, size):
    Limbs = [['  ', "##", "@@", "££", "$$", "__"], ["'", "^", "!"],
             ['0', 'o', '_', '-', '=', '~'], ['/', '\l'[0], '|']]
    
    pomPom = ChooseFrom(Limbs[0])
    eye = ChooseFrom(Limbs[1])
    mouth = ChooseFrom(Limbs[2])
    leftLeg = ChooseFrom(Limbs[3])
    rightLeg = ChooseFrom(Limbs[3])
    
    # Create new Cheerers every time.
    # Or based on occasion.
    if "!RUN!" in Banner[1]:
        pomPom = Limbs[0][4]
        eye = Limbs[1][1]
        mouth = Limbs[2][0]
        leftLeg = Limbs[3][2]
        rightLeg = Limbs[3][1]
    elif "[x]" in Banner[0]:
        pomPom = Limbs[0][0]
        eye = '*'
        mouth = 'x'
        leftLeg = Limbs[3][0]
        rightLeg = Limbs[3][1]
    
    if not pomPom == "__" and not pomPom == "  ":
        print()
    
    lineAmount = -1
    # This is ugly and unavoidable pretty sure.
    while size and not size == lineAmount:
        if size >= 4:
            lineAmount = 4
            size -= 4
        else:
            lineAmount = size
        
        if lineAmount:
            JC.Spam((pomPom + "     " + pomPom + ' ') * lineAmount
                    + ' __' + '_' * (len(Banner[0])) + '__ \n', 1,
                    round(JC.Delays[0] / 4), False)
            
            JC.Spam((" \(" + eye + mouth + eye + ")/  ") * lineAmount
                    + '|  ' + Banner[0] + '  | \n', 1, round(JC.Delays[0] / 4),
                    False)
            
            JC.Spam(("   ||     ") * lineAmount
                    + '|  ' + Banner[1] + '  | \n', 1, round(JC.Delays[0] / 4),
                    False)
            
            JC.Spam(("   " + leftLeg + rightLeg + "     ") * lineAmount + '|--'
                    + '-' * len(Banner[0]) + '--| \n', 1, round(JC.Delays[0] / 4),
                    False)
    print()
    JC.Pause(3)
    
JC.Release_Ready(["Intro On: " + JC.Yessify(Intro),
                  "Harsh Off: " + JC.Yessify(not Harsh),
                  "Checkpoint is 3 : " + JC.Yessify(checkpoint == 3),
                  "Shuffle Decks On: " + JC.Yessify(ShuffleDecks),
                  "File Explorer On: " + JC.Yessify(CanExplore),
                  "Deck File is 'Deck Data': " +
                   JC.Yessify(deckFolder + deckFile ==
                              "Your Decks\\Deck Data - 1.txt")])


# 'DEFAULT DECK FILE' CARDER START:
JC.Title(" Flash-Carder (PC): ")
JC.ErrorIf(not any(deckFile), "No default deck file was specified/coded in.")
JC.IsBusy("Loading default deck file: " + JC.Quote(deckFile), False)
Revising = True

while Revising:
    # 'Deck' takes the form
    # 'Deck[which question][which answer to the question]'
    Deck = [[]]
    NewCard = []
    
    # 'YOUR DECKS' FILE EXPLORER:
    if CanExplore and len(os.listdir(deckFolder)) > 1:
        if JC.OkayWith("\nChoose a different file?"):
            gap = ''
            deckAddress = 0
            JC.Pace('\n' + JC.Quote(deckFolder) + " Deck Folder:")
            
            # Build a kind of file tree...
            for file in os.listdir(deckFolder):
                print(' |')
                deckAddress += 1
                JC.DramaTypeHow('(' + str(deckAddress)
                                + ")--> '" + file + "'", JC.dramaSpeed*1.5)
                print()
            print()
            
            deckAddress = \
                int(input("Which file number would you like to load?" + JC.cursor))
            
            # Cut off the tree part to get the deck file name...
            deckFile = os.listdir(deckFolder)[deckAddress - 1]
            print()
            
            JC.IsBusy("Loading new deck file: " + JC.Quote(deckFile), False)
        else:
            JC.Pace("\nOkay end = ''")
            JC.IsBusy(" Resuming loading " + JC.Quote(deckFile), False)
            
    deckFile = deckFolder + deckFile
    
    # 'DECK DATA' FILE READER:
    JC.FreshPage()
    
    # 'Deck[0]': An array where each item is a line
    # of data, is added as a single 'Deck[0]' item.
    Deck[0] = JC.TryToRead(deckFile).split('\n')
    
    # Detect Empty + Same Bullet errors.
    JC.ErrorIf(questionBullet == answerBullet or \
                questionBullet == commentBullet or \
                   commentBullet == answerBullet,
                   "At least 2 Deck File bullets were the same, but shouldn't be.")
    
    JC.ErrorIf(answerBullet and questionBullet in Deck[0],
                       "Empty question and/or answer bullets found.")
    
    JC.ErrorIf(questionBullet in Deck[0], "Empty question bullet(s) found.")
    
    JC.ErrorIf(JC.OneArrayed([answerBullet, questionBullet], Deck[0]),
                  "Empty answer bullet(s) found.")
            
    # Use 'NewCard' to help remove ignorable lines.
    for item in Deck[0]:
        if item in ['\t', '', ' '] or ItsA("Comment", item):
            NewCard.append(item)
        else:
            Deck[0][Deck[0].index(item)] = FixSpaces(item)
    JC.RemoveAll(NewCard, Deck[0])
    NewCard = []
    
    # Fixing 'Deck' arrays layout:
    partStart = -1
    for item in Deck[0]:
        if ItsA("New Question", item):
            # 'NewCard' is a de-bulleted array/dimension/question
            # and its answers, to be added individually to the 'Deck'.
            NewCard.append(item[len(questionBullet):])
            partStart += 1
    
        elif ItsA("New Answer", item):
            JC.ErrorIf(not any(NewCard),
                       "Expected question before answer, got the opposite.")
            NewCard.append(item[len(answerBullet):])
            partStart += 1
        else:
            # Must be a continued part, so add it to the original.
            JC.ErrorIf(partStart < 0, "Random Text found at the start of the Deck File")
            NewCard[partStart] = FixSpaces(NewCard[partStart] + item)
    
        if ItsA("Question Next", JC.TheItem("After", item, Deck[0])) \
                or JC.TheItem("Is The Last", item, Deck[0]):
            # A previous question was just finished. Add that one now.
            if JC.TheItem("Is The Last", item, Deck[0]):
                Deck.remove(Deck[0])
            Deck.append(NewCard)
            partStart = -1
            NewCard = []
            
    bestStreak = streak = 0
    initialDeckSize = len(Deck)
    cardsLeft = initialDeckSize
    
    # 'CUSTOM DECK' CARDER START:
    JC.Title(JC.Quote(deckFile[deckFile.index('\ '[0]) + 1:]) + " Flash-Carder:")
    JC.AssertDominance()
    JC.Pace("(There are " + str(initialDeckSize) + " questions)")
    
    if Intro:
        JC.TitledList("Commands List", Commands, False)
        JC.CatchUp()
        JC.FreshPage()
    
    JC.IsBusy("Starting", True)
    
    # CARD-FLASH LOOP:
    while any(Deck):
        # (RE)SETTING:
        TheAnswers = []
        CorrectAnswers = []
        NewCard = Deck[0]
        MyInputs = []
        
        # Pick Question.
        if ShuffleDecks:
            NewCard = ChooseFrom(Deck)
            
        # Everything apart from the question title
        # (from NewCard[1] upwards and inclusive) is answers.
        TheAnswers = NewCard[1:]
            
        if streak and JC.AMultiple(streak, checkpoint):
            if streak == checkpoint:
                JC.Pace("{ Erm, a Crowd has appeared. }")
            else:
                JC.Pace("{ The Crowd is growing!? }")
                
            Crowd(["  Get A  ",
                          "!PERFECT!"], int(streak/2))
            
            JC.Pace("I guess we should keep them happy. Anyways.\n")
            JC.Pause(1)
        
        # ASK QUESTION:
        JC.Spam(">", 2, JC.Delays[0], False)
        JC.Pace(' ' + NewCard[0])
    
        if len(TheAnswers) > 1:
            JC.Pace(" * There are " + str(len(TheAnswers))
                    + " answers/parts to this question. *")
        print()
        
        Answering = True
        
        # GET ANSWERS:
        while Answering:
            response = JC.GetInput("Your answer", JC.BOTslowIterate(TheAnswers, ''))
            
            # Detect Commands.
            if JC.Commanded('commands', response):
                JC.TitledList("Commands List", Commands, False)
                JC.Pause(0)
            elif not any(response):
                if any(MyInputs):
                    Answering = False
                elif JC.OkayWith("Skip Question?"):
                    Answering = False
            # Or accept and save answer.
            else:
                MyInputs.append(response)
        JC.FreshPage()
        JC.Pause(0)
        
        # MARKING:
        if any(MyInputs):
            JC.IsBusy("Marking Answers", True)
        
        for myAnswer in MyInputs:
            # Check it against every actual answer...
            for thisAnswer in TheAnswers:
                ItsCorrect = JC.Pure(myAnswer) == JC.Pure(thisAnswer)
                
                # If a long, but not perfect answer, check word for word.
                if not ItsCorrect and len(AnswerWords) >= 9:
                    AnswerWords = thisAnswer.split(' ')
                    CheckedWords = []
                    wordsCorrect = 0
                    
                    for word in AnswerWords:
                        
                        # If I used the answerWord in myAnswer
                        # and it hasn't already been checked...
                        if word in JC.Pure(myAnswer).split(' ') and \
                                not AnswerWords.index(word) in CheckedWords:
                            CheckedWords.append(AnswerWords.index(word))
                            wordsCorrect += 1
                            
                    # If 80% of AnswerWords are in myAnswer, allow it.
                    ItsCorrect = (wordsCorrect >= round(0.8 * len(AnswerWords)))
                # If the myAnswer is perfect or allowed, ultimately...
                if ItsCorrect:
                    CorrectAnswers.append(myAnswer)
        # Then the whole question's correct when...
        ItsCorrect = len(CorrectAnswers) == len(TheAnswers)
        
        # FEEDBACK:
        if ItsCorrect:
            JC.Pace('[ ' + ChooseFrom(Remarks[ChooseFrom([0, 2])]) + '! ]')
            print()
        else:
            # If not skipped...
            if any(MyInputs):
                JC.Pace("[ err... ]")
                
            print('\n\t' + JC.listStart + "The answers were:" + JC.listEnd)
            JC.List(TheAnswers, False)
        
        print('\t' + JC.listStart + "Your entries were:" + JC.listEnd)
        JC.Pause(1)
        
        for myAnswer in MyInputs:
            JC.DramaType("\t- " + myAnswer)
            if JC.Pure(myAnswer) in list(map(JC.Pure, TheAnswers)):
                JC.DramaType("\t<- Perfect!")
            elif myAnswer in CorrectAnswers:
                JC.DramaType("\t<- I'll allow that...")
            print()
            JC.Pause(0)
        JC.Pause(1)
        #  ____
        # | Q2 \
        
        # MARKING FAIL-SAFE:
        if any(MyInputs) and not (ItsCorrect or Harsh):
            ItsCorrect = JC.OkayWith("\nWas your answer(s) actually correct?")
            if ItsCorrect:
                JC.DramaType("Oh, sorry: ")
                JC.IsBusy("Registering as Correct", False)
            else:
                print()
            
        # REMOVE LEARNT QUESTION:
        if ItsCorrect:
            streak += 1
            Deck.remove(NewCard)
            cardsLeft = len(Deck)
            
            # Streak mods...
            if any(Deck) and streak >= checkpoint:
                if streak > bestStreak:
                    bestStreak = streak
                if streak >= (checkpoint - 1):
                    JC.Pace("\n< On a " + str(streak) + " answer streak, " +
                            ChooseFrom(Remarks[ChooseFrom([1, 2])]) + "! > end = ''")
                else:
                    JC.Pace("\n< On a " + str(streak) + " answer streak! > end = ''")
                    
                if streak == round(0.60 * initialDeckSize):
                    JC.Pace("\nYou've nearly got a PERFECT RUN, Keep going!")
                    
                # Don't allow user correction.
                if Harsh:
                    print()
                    JC.CatchUp()
                    
            JC.Inform("Completed " + str(initialDeckSize - cardsLeft) + '/' +
                      str(initialDeckSize) + " questions. (~" +
                      str(round(100 - (100 * cardsLeft / initialDeckSize))) + '%)')
                    
        # Or if incorrect, lose Crowd...
        else:
            if streak >= checkpoint:
                # Upset Crowd...
                JC.Pace("\nWait, you lost the " + str(streak) + " streak!?")
        
                Crowd(["|[x]\ /[x]|",
                              " \ (===) / "], int(streak / checkpoint))
        
                JC.Pace("(Looks like the Crowd's leaving now...)")
                JC.Pause(1)
            streak = 0
        
        # NEXT QUESTION:
        if any(Deck):
            if ShuffleDecks or any(MyInputs):
                JC.IsBusy("Next Question", True)
            else:
                JC.IsBusy("Retrying Question", True)
                
            JC.FreshPage()
      
    # FINISH OFF:
    JC.FreshPage()
    JC.Pause(2)
    JC.Pace("\nAll Cards Learnt:  end = ''")
    
    # If Perfect, Crowd goes Wild!!
    if streak == initialDeckSize:
        JC.Pace("And a PERFECT RUN!!")
        JC.Inform("The Crowd Goes WIIILD!")
        
        Crowd(["!PERFECT!",
                      "  !RUN!  "], int(streak/checkpoint) + 3)
    else:
        JC.Pace("\n\n< This time, your largest streak was " + str(bestStreak) + " strong! > ")
        Crowd(["get a perfect",
                      "next time... "], 1)
        
    JC.Pace("Well Done!")
    
    JC.TitledList("Final Options", ["Load another card file", "End the Flash-Carder"], 1)
    if JC.TillSure('', 2) == '2':
        Revising = False
    
JC.GoAway()
