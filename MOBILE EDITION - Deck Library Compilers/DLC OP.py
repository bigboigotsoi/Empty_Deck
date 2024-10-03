import JCLib
import os
import re
from pathlib import Path


# BOOL MODS: Change these as you wish.

newbie = False
# PyIDLE = False
Tabbing = True
SpeedType = 1  # 1 Slowest, 3 fastets
deckFolder = Path("My Decks")

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



# FUNCTIONAL FUNCTIONS:
def Give_Guidance():
    JCLib.Pace(
        "\t'Converts deck Files in the " + deckFolder.name + " folder into a 'deck Library' format.")
    JCLib.Pace("\t(For Flash-carder Mobile only)")
    
    JCLib.Pace(
        "\n\tCopy the resulting deck Dictionary (or dictionary field) into "
        "the source code of your 'Flash Carder (Mobile)' program.'")
    
    JCLib.Notify(
            "When converting all deck files, they must all use the same bullet layout."
            + "\nIf they're different, please convert each file individually.")
    print()


def Which_Path(deckFolder, mode = None):
    deck_files = list(
        map(lambda directory: directory.name, deckFolder.iterdir()))
    
    JCLib.Wipe_CLI()
    
    if mode == 1:
        deckNumber = 0
        print("\n / Pre-loaded Decks:")
        JCLib.Pause(2)
        
        # Build a kind of file tree...
        for deckFile in deck_files:
            print(' |')
            JCLib.Pause(0)
            deckNumber += 1
            
            if Path(deckFolder / deckFile).is_dir():
                print(' ' + str(deckNumber) + "  [", deckFile, "]")
            else:
                print(' ' + str(deckNumber) + "  '" + deckFile + "'")
        
        print("/ ")
        JCLib.Pause(1)
        deckNumber = int(JCLib.Get_Input("\nChoose a File or [ Folder ]"))
        print()
        
        if Path(deckFolder / deck_files[deckNumber - 1]).is_dir():
            Which_Path(Path(deckFolder / deck_files[deckNumber - 1]), mode)
        else:
            return [deck_files[deckNumber - 1]]
    else:
        return deck_files


def SetDefaultBullets():


def LearnBullets():
    
    # messages =
    
    if not JCLib.Okay_With("Does the file(s) use the default bullet layout?"
                            " \n(Default layout uses '> ', '- ', '# ' bullets)"):
        
        BulletFor = {"Questions": "<same>", "Answers": "<same>", "Comments": "<same>"}
        print("Please specify the file(s) bullets", end = '')
        JCLib.DramaType('...\n')
    
        while not len(set(list(BulletFor.values()))) == 3:
            if not JCLib.One_Listed(["<same>"], [BulletFor["Questions"], BulletFor["Answers"]]):
                JCLib.Pace("Bullets cannot be the same")
            
            for bullet_type in BulletFor:
                BulletFor[bullet_type] = JCLib.Get_Input('(For ' + bullet_type + ')')
                
        return BulletFor
    else:
        return {"Questions": '> ', "Answers": '- ', "Comments": '# '}


def ReadAndVerified(fileName, FolderFileNames, BulletFor):
    DeckFile = deckFolder + FolderFileNames[FolderFileNames.index(fileName)]
    
    # Read the file but ignore comments and empty lines...
    DeckFile = list(filter(lambda Line: any(JCLib.Stripped(Line)) and
                                        not ItsA("Comment", Line, BulletFor),
                           JCLib.Try_Read(DeckFile)))
    
    # Detect file/bullet errors...
    JCLib.Error_When(
        JCLib.One_Listed([BulletFor["Questions"], BulletFor["Answers"]], DeckFile),
        "Empty question and/or answer bullet(s) found.")
    
    JCLib.Error_When(ItsA("Answer", DeckFile[0], BulletFor),
               "Expected question before answer, got the opposite.")
    print()
    
    return DeckFile


def Parse_Decks(parent_path):
    for path in parent_path:
        if SpeedType < 3:
            JCLib.Doing("Converting File: " + fileName)
    
        # SETTING UP: deck File.
        DeckFile = ReadAndVerified(fileName, FolderFileNames, BulletFor)
        DeckArray, lineNumber, QuestionsLeft = '[', 0, True
    
        if FirstTime:  # First file, no newline
            LibraryField = '"' + fileName[:len(fileName) - 4] + '": '
        else:
            LibraryField = Newline_Before(
                New_Level('"' + fileName + '": '))
    
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
                        JCLib.TheItem("After", thisLine, DeckFile))
            
                CompleteAnswer = ItsA("Answer", thisLine,
                                      BulletFor) and not \
                                     ContinuingAnswer(
                                             JCLib.TheItem("After",
                                                           thisLine,
                                                           DeckFile))
            
                # RE-FORMAT AND ADD ANSWERS:
                if CompleteAnswer:
                    # It's already complete, so just add with quotes.
                    DeckArray += Quote(FixSpaces(
                            re.sub(BulletFor["Answers"], '', thisLine)))
                
                    # If another answer is next, add a comma.
                    if ItsA("Answer",
                            JCLib.TheItem("After", thisLine, DeckFile),
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
                            JCLib.TheItem("After", thisLine, DeckFile)):
                        # Add it as the one, long, grown answer.
                        DeckArray += Quote(GrowingAnswer)
                        GrowingAnswer = ''
                        if ItsA("New Answer",
                                JCLib.TheItem("After", thisLine,
                                              DeckFile),
                                BulletFor):
                            DeckArray = Comma_After(DeckArray)
            
                # If the last answer for the question, or complete last answer...
                if ItsA("Question Coming Next",
                        JCLib.TheItem("After", thisLine, DeckFile),
                        BulletFor) \
                        or JCLib.TheItem("Is Last", thisLine, DeckFile):
                    DeckArray += ']'
                    if not JCLib.TheItem("Last", thisLine, DeckFile):
                        DeckArray = Comma_After(DeckArray)
                    AddingAnswers = False
            
                lineNumber += 1
        
            # Now we're done with adding answers, this question's finished.
        
            if JCLib.TheItem("Is the Last Line of the File", thisLine,
                             DeckFile):
                DeckArray += ']'
                if not JCLib.TheItem(
                        "Is the Last File in the deck Folder",
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
                    JCLib.DotDot()
                    print("  '" + DeckFile[0] + "'")
    
        # And now, done with all the questions in this file.
    
        if SpeedType <= 2:
            JCLib.Pause(1)
            print("\n\t* Completed Conversion! * ~"
                  + str(round(
                    100 * (FolderFileNames.index(fileName) + 1) / len(
                            FolderFileNames))) + "%")
            JCLib.Pause(2)
            print()

    # Finally, Library finished, no more files left!

    if ConvertingAll:
        print("* deck Library Created! *")
        JCLib.WindowRefresh()
        JCLib.Pause(2)
        print('\n' + DeckLibrary)
    else:
        print("* Library Field Created! *")
        JCLib.WindowRefresh()
        JCLib.Pause(2)
        print('\n' + LibraryField)

    JCLib.Pause(3)
    JCLib.Get_Input("\nType to Finish", 1)
    JCLib.GoAway()
    

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
    if "question" in JCLib.Stripped(what):
        bullet = BulletFor["Questions"]
    if "answer" in JCLib.Stripped(what):
        bullet = BulletFor["Answers"]
    
    if re.match(bullet, phrase):
        matched = True
    return matched


if __name__ == "__main__":
    JCLib.Title("deck File to deck Library Converter")
    if newbie:
        Give_Guidance()
    
    while True:
        # (RE)SETTING UP: deck Library.
        DeckLibrary, QuestionsLeft, FirstTime = "DeckLibrary = {", True, True
        
        ConvertingAll = JCLib.Menu_Response("Would you like to convert...",
                                   ["A single deck file.",
                                    "All deck files in the '" + deckFolder.name + "' folder."]) - 1
        BulletFor = LearnBullets()
        
        if ConvertingAll:
            FolderFileName = Which_Path(deckFolder),
            
    # if mode is None:
    #     mode =
        
        
        
        for fileName in deckFolder:
            if SpeedType < 3:
                JCLib.Doing("Converting File: " + fileName)
            
            # SETTING UP: deck File.
            BulletFor = LearnBullets()
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
                        JCLib.TheItem("After", thisLine, DeckFile))
                    
                    CompleteAnswer = ItsA("Answer", thisLine, BulletFor) and not \
                        ContinuingAnswer(
                            JCLib.TheItem("After", thisLine, DeckFile))
                    
                    # RE-FORMAT AND ADD ANSWERS:
                    if CompleteAnswer:
                        # It's already complete, so just add with quotes.
                        DeckArray += Quote(FixSpaces(
                            re.sub(BulletFor["Answers"], '', thisLine)))
                        
                        # If another answer is next, add a comma.
                        if ItsA("Answer",
                                JCLib.TheItem("After", thisLine, DeckFile),
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
                                JCLib.TheItem("After", thisLine, DeckFile)):
                            # Add it as the one, long, grown answer.
                            DeckArray += Quote(GrowingAnswer)
                            GrowingAnswer = ''
                            if ItsA("New Answer",
                                    JCLib.TheItem("After", thisLine, DeckFile),
                                    BulletFor):
                                DeckArray = Comma_After(DeckArray)
                    
                    # If the last answer for the question, or complete last answer...
                    if ItsA("Question Coming Next",
                            JCLib.TheItem("After", thisLine, DeckFile), BulletFor) \
                            or JCLib.TheItem("Is Last", thisLine, DeckFile):
                        DeckArray += ']'
                        if not JCLib.TheItem("Last", thisLine, DeckFile):
                            DeckArray = Comma_After(DeckArray)
                        AddingAnswers = False
                    
                    lineNumber += 1
                
                # Now we're done with adding answers, this question's finished.
                
                if JCLib.TheItem("Is the Last Line of the File", thisLine,
                              DeckFile):
                    DeckArray += ']'
                    if not JCLib.TheItem("Is the Last File in the deck Folder",
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
                        JCLib.DotDot()
                        print("  '" + DeckFile[0] + "'")
            
            # And now, done with all the questions in this file.
            
            if SpeedType <= 2:
                JCLib.Pause(1)
                print("\n\t* Completed Conversion! * ~"
                      + str(round(
                    100 * (FolderFileNames.index(fileName) + 1) / len(
                        FolderFileNames))) + "%")
                JCLib.Pause(2)
                print()
        
        # Finally, Library finished, no more files left!
        
        if ConvertingAll:
            print("* deck Library Created! *")
            JCLib.WindowRefresh()
            JCLib.Pause(2)
            print('\n' + DeckLibrary)
        else:
            print("* Library Field Created! *")
            JCLib.WindowRefresh()
            JCLib.Pause(2)
            print('\n' + LibraryField)
        
        JCLib.Pause(3)
        JCLib.Get_Input("\nType to Finish", 1)
        JCLib.GoAway()