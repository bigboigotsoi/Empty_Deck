import JC
import os
import re


# BOOL MODS: Change these as you wish.

Intro = False
# PyIDLE = False
Tabbing = True
SpeedType = 1  # 1 Slowest, 3 fastets
deckFolder = "My Decks\\"

biggestTab = ''
if Tabbing:
    biggestTab = '\t'
# elif not PyIDLE:
#     biggestTab = '\t\t\t\t\t'
#     # (Tabs are inconsistent cross-platform)

# LAMBDAS: Necessary for clarity.
Quote = lambda term: '"' + term + '"'
Comma_After = lambda line: line + ', '

Newline_Before = lambda line: '\n' + line
New_Level = lambda line: Newline_Before(biggestTab + line)

ContinuingAnswer = lambda line: any(line) and not (
            ItsA("Question", line, BulletFor)
            or ItsA("Answer", line, BulletFor))


# PRACTICAL FUNCTIONS:
def FixSpaces(phrase):
    while '  ' in phrase:
        phrase = phrase.replace('  ', ' ')
    while '\t' in phrase:
        phrase = phrase.replace('\t', ' ')
    while '\n' in phrase:
        phrase = phrase.replace('\n', ' ')
    return phrase


def ItsA(what, phrase, BulletFor):
    # Finds out by checking the bullet region/slice of the phrase.
    matched = False
    bullet = BulletFor["Comments"]
    if "question" in JC.Pure(what):
        bullet = BulletFor["Questions"]
    if "answer" in JC.Pure(what):
        bullet = BulletFor["Answers"]
    
    if re.match(bullet, phrase):
        matched = True
    return matched


# FUNCTIONAL FUNCTIONS:
def Start(Intro):
    JC.Title("deck Folder -> Library Converter")
    
    if Intro:
        JC.SmartPace(
            "\t'Converts deck Files in the " + deckFolder + " folder into a 'deck Library' format.")
        JC.SmartPace("\t(For Flash-carder Mobile only)")
        
        JC.SmartPace(
            "\n\tCopy the resulting deck Dictionary into the source code of your 'Flash Carder (Mobile)' "
            "program.'")
        print()


def SetDefaultBullets():
    # if JC.OkayWith("Do all deck files in the '" + deck_folder + "' folder use the same bullet layout?"):
    #     if JC.OkayWith("Do they all use the default bullet layout? \n(Default layout uses '> ', '- ', '# ' bullets)"):
    #         JC.Pace("\nOkay.\n")
    return False, {"Questions": '> ', "Answers": '- ', "Comments": '# '}
    JC.Pace("\nOkay Then.\n")
    # return True, {"Questions": None, "Answers": None, "Comments": None}


def WhichDeck(deckFolder):
    FolderFileNames = os.listdir(deckFolder)
    
    JC.TitledList("Would you like to...",
                  ["Convert the entire deck folder into the deck library?",
                   "Convert one deck file to a deck library field"], 1)
    if JC.GetInput('', 1) == '2':
        deckNumber = 0
        print("\n / Pre-loaded Decks:")
        JC.Pause(2)
        
        # Build a kind of file tree...
        for deckFile in FolderFileNames:
            deckNumber += 1
            print(' |')
            JC.Pause(0)
            print('[' + str(deckNumber) + "]-- '" + deckFile + "'")
            JC.Pause(0)
        JC.Pause(3)
        
        deckNumber = 200
        while not JC.InRange(1, deckNumber, len(FolderFileNames)):
            deckNumber = int(input("\nPlease choose a deck File:- "))
            print()
        
        return [FolderFileNames[deckNumber - 1]], False
    return FolderFileNames, True


def LearnBullets(LearningBullets):
    if LearningBullets:
        print("Please specify this file's", end = '')
        JC.DotDot()
        print()
        
        while BulletFor["Questions"] == BulletFor["Answers"]:
            if any(BulletFor["Questions"]) or any(BulletFor["Answers"]):
                JC.Pace("Bullets cannot be the same")
            
            BulletFor["Questions"], BulletFor["Answers"], BulletFor[
                "Comments"] = (
                    JC.GetInput("Question bullet", '> '),
                    JC.GetInput("Answer bullet", '- '),
                    JC.GetInput("Comment bullet", '# '))
    
    return BulletFor


def ReadAndVerified(fileName, FolderFileNames, BulletFor):
    DeckFile = deckFolder + FolderFileNames[FolderFileNames.index(fileName)]
    
    # Read the file but ignore comments and empty lines...
    DeckFile = list(filter(lambda Line: any(JC.Pure(Line)) and
                                        not ItsA("Comment", Line, BulletFor),
                           JC.TryToRead(DeckFile)))
    
    # Detect file/bullet errors...
    JC.ErrorIf(
        JC.OneArrayed([BulletFor["Questions"], BulletFor["Answers"]], DeckFile),
        "Empty question and/or answer bullet(s) found.")
    
    JC.ErrorIf(ItsA("Answer", DeckFile[0], BulletFor),
               "Expected question before answer, got the opposite.")
    print()
    
    return DeckFile


if __name__ == "__main__":
    Start(Intro)
    
    while True:
        # (RE)SETTING UP: deck Library.
        DeckLibrary, QuestionsLeft, FirstTime = "DeckLibrary = {", True, True
        LearningBullets, BulletFor = SetDefaultBullets()
        FolderFileNames, ConvertingAll = WhichDeck(deckFolder)
        
        for fileName in FolderFileNames:
            if SpeedType < 3:
                JC.IsBusy("Converting File: " + fileName, False)
            
            # SETTING UP: deck File.
            BulletFor = LearnBullets(LearningBullets)
            DeckFile = ReadAndVerified(fileName, FolderFileNames, BulletFor)
            DeckArray, lineNumber, QuestionsLeft = '[', 0, True
            
            if FirstTime:  # First file, no newline
                LibraryField = '"' + fileName[:len(fileName) - 4] + '": '
            else:
                LibraryField = Newline_Before(New_Level('"' + fileName + '": '))
            
            while QuestionsLeft:
                # (RE)SETTING UP: Lines. Done questions are removed too
                DeckFile, AddingAnswers, GrowingAnswer, thisLine, \
                lineNumber = DeckFile[lineNumber:], True, '', '', 0
                
                if not FirstTime:
                    DeckArray += Newline_Before('')
                DeckArray += New_Level('[')
                FirstTime = False
                
                # ADD DE-BULLETTED QUESTION:
                DeckArray += Comma_After(Quote(
                        re.sub(BulletFor["Questions"], '',
                               DeckFile[lineNumber]))) + New_Level(' ')
                
                # ADD ANSWERS:
                while AddingAnswers:
                    # Extract next answer...
                    thisLine = DeckFile[lineNumber]
                    
                    # Lambdas for clarity...
                    AnswerWillGrow = ContinuingAnswer(
                        JC.TheItem("After", thisLine, DeckFile))
                    
                    CompleteAnswer = ItsA("Answer", thisLine, BulletFor) and not \
                        ContinuingAnswer(
                            JC.TheItem("After", thisLine, DeckFile))
                    
                    # RE-FORMAT AND ADD ANSWERS:
                    if CompleteAnswer:
                        # It's already complete, so just add with quotes.
                        DeckArray += Quote(FixSpaces(
                            re.sub(BulletFor["Answers"], '', thisLine)))
                        
                        # If another answer is next, add a comma.
                        if ItsA("Answer",
                                JC.TheItem("After", thisLine, DeckFile),
                                BulletFor):
                            DeckArray = Comma_After(DeckArray)
                    
                    # Deal with growing, multi-line answers...
                    elif AnswerWillGrow or ContinuingAnswer(thisLine):
                        # Grow it more...
                        GrowingAnswer += re.sub(BulletFor["Answers"], '',
                                                thisLine)
                        GrowingAnswer = FixSpaces(GrowingAnswer)
                        
                        # When the answer is finished growing...
                        if not ContinuingAnswer(
                                JC.TheItem("After", thisLine, DeckFile)):
                            # Add it as the one, long, grown answer.
                            DeckArray += Quote(GrowingAnswer)
                            GrowingAnswer = ''
                            if ItsA("New Answer",
                                    JC.TheItem("After", thisLine, DeckFile),
                                    BulletFor):
                                DeckArray = Comma_After(DeckArray)
                    
                    # If the last answer for the question, or complete last answer...
                    if ItsA("Question Coming Next",
                            JC.TheItem("After", thisLine, DeckFile), BulletFor) \
                            or JC.TheItem("Is Last", thisLine, DeckFile):
                        DeckArray += ']'
                        if not JC.TheItem("Last", thisLine, DeckFile):
                            DeckArray = Comma_After(DeckArray)
                        AddingAnswers = False
                    
                    lineNumber += 1
                
                # Now we're done with adding answers, this question's finished.
                
                if JC.TheItem("Is the Last Line of the File", thisLine,
                              DeckFile):
                    DeckArray += ']'
                    if not JC.TheItem("Is the Last File in the deck Folder",
                                      fileName, FolderFileNames):
                        DeckArray = Comma_After(DeckArray)
                    elif ConvertingAll:
                        DeckArray += '}'
                    
                    LibraryField += DeckArray
                    DeckLibrary += LibraryField
                    QuestionsLeft = False
                
                if SpeedType == 1:
                    if FirstTime:
                        print("\t* Added Question: '" + DeckFile[0] + "' *")
                    else:
                        print(biggestTab + " ", end = '')
                        JC.DotDot()
                        print("  '" + DeckFile[0] + "'")
            
            # And now, done with all the questions in this file.
            
            if SpeedType <= 2:
                JC.Pause(1)
                print("\n\t* Completed Conversion! * ~"
                      + str(round(
                    100 * (FolderFileNames.index(fileName) + 1) / len(
                        FolderFileNames))) + "%")
                JC.Pause(2)
                print()
        
        # Finally, Library finished, no more files left!
        
        if ConvertingAll:
            print("* deck Library Created! *")
            JC.WindowRefresh()
            JC.Pause(2)
            print('\n' + DeckLibrary)
        else:
            print("* Library Field Created! *")
            JC.WindowRefresh()
            JC.Pause(2)
            print('\n' + LibraryField)
        
        JC.Pause(3)
        JC.GetInput("\nType to Finish", 1)
        JC.GoAway()