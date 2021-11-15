from random import choice as ChooseFrom
from re import sub as Replace
import JCLib
import os


# Carder iterates through the
# 'deck' Array and tests you.

# Correctly answered questions
# are removed until none are left.

# Runs until full marks, so when 
# the 'deck' Array is empty.

# VARIABLES/DATA:
Intro = True
Harsh = False
Can_Explore = True
ShuffleDecks = True


# Directory + name of the DEFAULT data file.
deck_folder = "My Decks"
deck_file = "Colossians 3"

questionBullet = '> '
answerBullet = '- '
commentBullet = '# '

checkpoint = 3


remarks = [
        # Correct answer remarks...
        ["Yep", "Correctumundo", "Mate, spot on", "You're decent at this",
         "Wowee Correct", "Correct", "Obviously, correct", "Alright mate",
         "There's no fooling you", "I'll give you that", "Bang on",
         "Pretty much", "Perfect", "Good choice", "You remembered that one"],
        
        # remarks for new streaks...
        ["That's crazy", "Now that's impressive", "Take care of it",
         "Don't lose it", "That's pretty big", "At least it's not " +
         ChooseFrom(["zero", "nothing"]) + "Better than " +
         ChooseFrom(["zero", "nothing"]) + " I guess", "Look after it okay",
         "Keep it safe", "That's unreal", "Didn't think you'd get this far",
         "I'm actually surprised", "Wasn't expecting that", "You cheated",
         "You'll lose it soon anyway", "Bet it won't last though"],
        
        # remarks for new streaks and correct answers....
        ["Great", "Keep it up", "Nice one", "Nicely Done", "Get in there mate",
         "Keep it up", "Hey... that's pretty good", '', "Lets gooo",
         "You're getting good at this", "EZ", "ez", "gg ez", "2 ez",
         "Easy", "That's half-decent", "You're on it today", "Looking good"]]

commands = ["'Enter'     :>  Finish answering.",
            "'commands'  :>  See commands List"]

done_decks = []



# Functions...

quote = lambda message: '"' + message + '"'

def Fix_Spaces(phrase):
    while '  ' in phrase:
        phrase = phrase.replace('  ', ' ')
    while '\t' in phrase:
        phrase = phrase.replace('\t', ' ')
    while '\n' in phrase:
        phrase = phrase.replace('\n', ' ')

    return phrase

def Its_A(what, phrase):
    global questionBullet
    global answerBullet
    
    # Finds out by checking the bullet region/slice of the phrase.
    if "question" in JCLib.Stripped(what):
        bullet = questionBullet
        return phrase[:len(questionBullet)] == questionBullet
    elif "answer" in JCLib.Stripped(what):
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
            JCLib.DramaType((pomPom + "     " + pomPom + ' ') * lineAmount
                    + ' __' + '_' * (len(Banner[0])) + '__ \n', 1,
                    round(JCLib.Delays[0] / 4), False)
            
            JCLib.DramaType((" \(" + eye + mouth + eye + ")/  ") * lineAmount
                    + '|  ' + Banner[0] + '  | \n', 1, round(JCLib.Delays[0] / 4),
                    False)
            
            JCLib.DramaType(("   ||     ") * lineAmount
                    + '|  ' + Banner[1] + '  | \n', 1, round(JCLib.Delays[0] / 4),
                    False)
            
            JCLib.DramaType(("   " + leftLeg + rightLeg + "     ") * lineAmount + '|--'
                    + '-' * len(Banner[0]) + '--| \n', 1, round(JCLib.Delays[0] / 4),
                    False)
    print()
    JCLib.Pause(3)

def Strip_Answer(phrase):
    while phrase[len(phrase) - 1] in ['.', ',', '!', '?']:
        phrase = phrase[:len(phrase) - 1]
    return phrase.lower()

def Search_Folder(current_folder):
    deck_address = 0
    JCLib.Pace("\n'" + current_folder + "' DECK FOLDER:\n")

    # Build a kind of file tree...
    for element in os.listdir(current_folder):
        deck_address += 1
        labels = ['   ', '']
        choice_directory = current_folder + '\\' + element

        if not deck_address == 1:
            print('|')

        if os.path.isdir(choice_directory):
            labels = ['   [ ', ' ]']

        if os.path.basename(element) in done_decks:
            labels[1] += '{:>50}'.format(': DONE!')
        elif os.path.isdir(choice_directory):
            labels[1] += '{:>50}'.format(': ' + str(len(os.listdir(choice_directory))) + ' Files')
        else:
            labels[1] += '{:>50}'.format(' : ' + str(' '.join(JCLib.Try_Read(choice_directory)).count('>')) + ' Qs')

        # Display...
        print(str(deck_address) + ('{}' + Replace('.txt', '', os.path.basename(element)) + '{}').format(*labels))
        JCLib.Pause(0)
    print('/ ')

    JCLib.Pause(1)
    print()
    deck_address = int(JCLib.Get_Input("Which item number would you like to load?"))
    choice_directory = current_folder + '\\' + os.listdir(current_folder)[deck_address - 1]

    if not os.path.isdir(choice_directory):  # Base Case: When a deck is reached
        return choice_directory
    else:
        # Recursive Call
        JCLib.Doing("Searching '" + os.path.basename(choice_directory), newlines=1)
        return Search_Folder(choice_directory)

JCLib.Release_Ready(["Intro On: " + JCLib.Yessify(Intro),
                  "Harsh Off: " + JCLib.Yessify(not Harsh),
                  "Checkpoint is 3 : " + JCLib.Yessify(checkpoint == 3),
                  "Shuffle Decks On: " + JCLib.Yessify(ShuffleDecks),
                  "File Explorer On: " + JCLib.Yessify(Can_Explore),
                  "deck File is 'deck Data': " +
                   JCLib.Yessify(deck_folder + deck_file ==
                              "Your Decks\\deck Data - 1.txt")])



# 'DEFAULT DECK FILE' CARDER START:
JCLib.Title(" Flash-Carder (Standard Edition): ")

JCLib.Doing("Loading default deck file: " + quote(deck_file), newlines=1)
JCLib.Error_When(not any(deck_file), "No default deck file was specified/coded in.")
Revising = True


while Revising:
    # 'deck' takes the form 'deck[which question][which answer to the question]'
    deck = [None]
    current_card = []
    
    # 'YOUR DECKS' FILE EXPLORER:
    if Can_Explore and len(os.listdir(deck_folder)) > 1:
        if JCLib.Okay_With("\nChoose a different file?"):
            deck_file = Search_Folder(deck_folder)
            JCLib.Doing("Loading new deck file: " + quote(deck_file))
        else:
            deck_file = deck_folder + '\\' + deck_file


    # 'DECK DATA' FILE READER:
    JCLib.Wipe_CLI()

    # 'deck[0]': Contains an array where each item is a line of the deck file
    deck[0] = JCLib.Try_Read(deck_file)
    
    # Detect Empty + Same Bullet errors.
    JCLib.Error_When(questionBullet == answerBullet or \
                questionBullet == commentBullet or \
                   commentBullet == answerBullet,
                   "At least 2 deck File bullets were the same, but shouldn't be.")
    
    JCLib.Error_When(JCLib.One_Listed([questionBullet, answerBullet], deck[0]),
                       "Empty question and/or answer bullet(s) found.")
            
    # Use 'current_card' to help remove ignorable lines.
    for item in deck[0]:
        if item in ['\t', '', ' '] or Its_A("Comment", item):
            current_card.append(item)
        else:
            deck[0][deck[0].index(item)] = Fix_Spaces(item)
    JCLib.Remove_All(current_card, deck[0])
    current_card = []
    
    # Fixing 'deck' arrays layout:
    partStart = -1
    for item in deck[0]:
        if Its_A("New Question", item):
            # 'current_card' is a de-bulleted array/dimension/question
            # and its answers, to be added individually to the 'deck'.
            current_card.append(item[len(questionBullet):])
            partStart += 1
    
        elif Its_A("New Answer", item):
            JCLib.Error_When(not any(current_card),
                       "Expected question before answer, got the opposite.")
            current_card.append(item[len(answerBullet):])
            partStart += 1
        else:
            # Must be a continued part, so add it to the original.
            JCLib.Error_When(partStart < 0, "Random Text found at the start of the deck File")
            current_card[partStart] = Fix_Spaces(current_card[partStart] + item)
    
        if Its_A("Question Next", JCLib.The_Item("After", item, deck[0])) \
                or JCLib.The_Item("Is The Last", item, deck[0]):
            # A previous question was just finished. Add that one now.
            if JCLib.The_Item("Is The Last", item, deck[0]):
                deck.remove(deck[0])
            deck.append(current_card)
            partStart = -1
            current_card = []
            
    bestStreak = streak = 0
    initialDeckSize = len(deck)
    cardsLeft = initialDeckSize
    
    # 'CUSTOM DECK' CARDER START:
    JCLib.Title(quote(deck_file[deck_file.index('\ '[0]) + 1:]) + " Flash-Carder  ")
    JCLib.Pace("\t(There are " + str(initialDeckSize) + " questions)")
    print()
    
    if Intro:
        JCLib.Titled_List("Commands List", commands, numbered=False, newlines=1)
        JCLib.Prompt()
        
    JCLib.Doing("Starting", newlines=1)
    JCLib.Wipe_CLI()
    
    # CARD-FLASH LOOP:
    while any(deck):
        # (RE)SETTING:
        MyInputs = []
        MatchedYet = []
        TheAnswers = [[], []]
        CorrectAnswers = [[], []]
        current_card = deck[0]


        # Pick Question.
        if ShuffleDecks:
            current_card = ChooseFrom(deck)
            
        # Everything apart from the question title (current_card[1] up inclusive) is answers.
        TheAnswers = current_card[1:]
            
        if streak and streak // checkpoint == 0:
            if streak == checkpoint:
                JCLib.Pace("{ Erm, a Crowd has appeared. }")
            else:
                JCLib.Pace("{ The Crowd is growing!? }")
                
            Crowd(["  Get A  ",
                          "!PERFECT!"], int(streak/checkpoint))
            
            JCLib.Pace("I guess we should keep them happy. Anyways.")
            JCLib.Pause(1)


        # ASK QUESTION:
        JCLib.DramaType(">>", Paced=True)
        JCLib.Pace(' ' + current_card[0])
    
        if len(TheAnswers) > 1:
            JCLib.Pace(" * There are " + str(len(TheAnswers[0])) + " answers/parts to this question. *")
        print()
        
        Answering = True


        # GET ANSWERS:
        while Answering:
            response = JCLib.Get_Input("Your answer")
            
            # Detect commands.
            if JCLib.Commanded('commands', response):
                JCLib.Titled_List("commands List", commands, False)
                JCLib.Pause(0)
            elif not any(response):
                if any(MyInputs):
                    Answering = False
                elif JCLib.Okay_With("Skip Question?"):
                    Answering = False
            # Or accept and save answer.
            else:
                MyInputs.append(response)
        JCLib.Wipe_CLI()
        JCLib.Pause(0)


        # MARKING:
        if any(MyInputs):
            JCLib.Doing("Marking Answers", True)
            
        # For every input...
        TheAnswers = [TheAnswers, list(map(JCLib.Stripped, current_card[1:]))]
        for myAnswer in MyInputs:
            CountedCorrect = False
            # Check it against every true pure answer.
            for thisAnswer in TheAnswers[1]:
                if TheAnswers[1].index(thisAnswer) not in CorrectAnswers[1]:
                    CountedCorrect = JCLib.Stripped(myAnswer) == thisAnswer
                    thisAnswer = thisAnswer.split(' ')
        
                    # If not perfect and a long answer, mark by-word...
                    if not CountedCorrect and len(thisAnswer) >= 4:
                        wordsCorrect = 0
                        MatchedYet.clear()
                        myAnswer = myAnswer.split(' ')
            
                        for answerWord in thisAnswer:
                            if answerWord in list(map(JCLib.Stripped, myAnswer)):
                                # If this specific occurrence of answerWord found in MY pure answer.
                                if list(map(JCLib.Stripped, myAnswer)).index(answerWord) not in MatchedYet:
                                    MatchedYet.append(list(map(JCLib.Stripped, myAnswer)).index(answerWord))
                                    wordsCorrect += 1
            
                        # So now, if 80% of AnswerWords are correct...
                        CountedCorrect = (wordsCorrect >= round(0.8 * len(thisAnswer)))
            
                        myAnswer = ' '.join(myAnswer)
                    thisAnswer = ' '.join(thisAnswer)
        
                    # Overall, if perfect or close...
                    if CountedCorrect:
                        CorrectAnswers[0].append(myAnswer)
                        CorrectAnswers[1].append(TheAnswers[1].index(thisAnswer))
        
                    # If myAnswer correct or I got the whole question correct
                    if CountedCorrect or len(CorrectAnswers[0]) == len(TheAnswers[0]):
                        # 'Break' returns to the first 'For' loop
                        # to select next input or exit marking...
                        break
                        
        # Marking resetting.
        TheAnswers = TheAnswers[0]
        CorrectAnswers = CorrectAnswers[0]
        
        # Then the whole question's correct when...
        CountedCorrect = len(CorrectAnswers) == len(TheAnswers)


        # FEEDBACK:
        if CountedCorrect:
            JCLib.Pace('[ ' + ChooseFrom(remarks[ChooseFrom([0, 2])]) + '! ]')
            print()
        else:
            # If not skipped...
            if any(MyInputs):
                print()
                JCLib.Pace("[ err... ]")
                
            JCLib.Titled_List("The answers were:", TheAnswers, numbered=False, tabs=1)
        
        if any(MyInputs):
            print('\t' + JCLib.listStart + "Your entries were:" + JCLib.listEnd)
            JCLib.Pause(1)
            Shown = []
        
            for myAnswer in MyInputs:
                JCLib.DramaType("\t- " + myAnswer + "    ")
                if myAnswer in Shown:
                    JCLib.DramaType("* found already *")
                if Strip_Answer(myAnswer) in list(
                        map(Strip_Answer, TheAnswers)) and myAnswer not in Shown:
                    JCLib.DramaType("\t<- Perfecto!")
                elif myAnswer in CorrectAnswers and myAnswer not in Shown:
                    JCLib.DramaType("\t<- I'll allow that...")
                print()
                JCLib.Pause(0)
        JCLib.Pause(1)
        
        #  ____
        # | Q2 \
        
        # MARKING FAIL-SAFE:
        if any(MyInputs) and not (CountedCorrect or Harsh):
            CountedCorrect = JCLib.Okay_With("\nWas your answer(s) actually correct?")
            if CountedCorrect:
                JCLib.DramaType("Oh, sorry: ")
                JCLib.Doing("Registering as Correct", False)
            
        # REMOVE LEARNT QUESTION:
        if CountedCorrect:
            streak += 1
            if streak > bestStreak:
                bestStreak = streak
            deck.remove(current_card)
            cardsLeft = len(deck)
            
            # Streak mods...
            if streak >= checkpoint:
                print("< On a " + str(streak) + " answer streak, ", end = '')
                if streak > checkpoint:
                    print(ChooseFrom(remarks[ChooseFrom([1, 2])]), end ='')
                print("! > end = ''")
                    
                if streak >= round(0.60 * initialDeckSize):
                    JCLib.Pace("\nYou've nearly got a PERFECT RUN, Keep going!")
                    
                # Don't allow user correction.
                if Harsh:
                    print()
                    JCLib.Prompt()
                    
            JCLib.Notify("Completed " + str(initialDeckSize - cardsLeft) + '/' +
                      str(initialDeckSize) + " questions. (~" +
                      str(round(100 - (100 * cardsLeft / initialDeckSize))) + '%)')
                    
        # Or if incorrect, lose Crowd...
        else:
            if streak >= checkpoint:
                # Upset Crowd...
                JCLib.Pace("\nWait, you lost the " + str(streak) + " streak!?")
        
                Crowd(["|[x]\ /[x]|",
                              " \ (===) / "], int(streak / checkpoint))
        
                JCLib.Pace("(Looks like the Crowd's leaving now...)")
                JCLib.Pause(1)
            streak = 0
        
        # NEXT QUESTION:
        if any(deck):
            if ShuffleDecks or any(MyInputs):
                JCLib.Doing("Next Question", True)
            else:
                JCLib.Doing("Retrying Question", True)
                
            JCLib.Wipe_CLI()
      
    # FINISH OFF:
    JCLib.Wipe_CLI()
    JCLib.Pause(2)
    JCLib.Pace("\nAll Cards Learnt:  end = ''")
    
    # If Perfect, Crowd goes Wild!!
    if streak == initialDeckSize:
        JCLib.Pace("And a PERFECT RUN!!")
        JCLib.Notify("The Crowd Goes WIIILD!")
        
        Crowd(["!PERFECT!",
                      "  !RUN!  "], int(streak/checkpoint) + 3)
    else:
        JCLib.Pace("\n\n< This time, your largest streak was " + str(bestStreak) + " strong! > ")
        Crowd([ "get a perfect",
                      "next time... "], 1)
        
    JCLib.Pace("Well Done!")

    if JCLib.Menu_Response("Final Options", ["Load another card file"], ["End the Flash-Carder"]) == '2':
        Revising = False
    
JCLib.End()
