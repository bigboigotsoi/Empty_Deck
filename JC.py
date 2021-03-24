import time

# Customize these variables
titleStart = titleEnd = " -- "
listStart = listEnd = "~ "
bullet = '- '
cursor = ':' + bullet

AIMBOT = False
Humanoid = False

FreshPages = False
DramaTyping = True

# Creating JC Timings..
BOTspeed = 15

# Define the largest pause, and
# Smaller ones will be auto-generated.
longPause = 1.25

Delays = [0, 0, 0, 0]
if longPause:
    if AIMBOT and not Humanoid:
        longPause = longPause / BOTspeed
    for count in range(4):
        # Decrease in size exponentially
        Delays.insert(0, round(longPause / 2 ** count, 2))
    del Delays[4:]

dramaDuration = Delays[1]

# Small helpful/nice looking lambdas
MaxIndex = lambda Array: len(Array) - 1
Commanded = lambda command, text: Pure(command) in Pure(text)
Digits = lambda number: len(str(number))
Quote = lambda phrase: "'" + phrase + "'"
AMultiple = lambda value, ofWhat: value and not value % ofWhat

# JC FUNCTIONS: In Categories of...

currentItem = -1

# 1 - PRESENTATION:

def WindowRefresh():
    if FreshPages:
        print('\n' * 38)
        
def Inform(message):
    EndCheck("\n* " + message + " * ", Buffered = True)

def IsBusy(theThing, Gapped):
    if Gapped:
        print()
    DotDot()
    print(str(theThing), end = '')
    DotDot()
    Pause(1)
    if Gapped:
        print()
    print()

def DramaTypeHow(message, duration):
    if DramaTyping:
        for character in message:
            print(character, end = '')
            time.sleep(duration / (len(message)))
    else:
        print(message)

DramaType = lambda message: DramaTypeHow(message, dramaDuration)

DotDot = lambda: DramaTypeHow('...', 0.20/BOTspeed)


# 2 - MESSAGING:

def An(controlNumber):
    if controlNumber == 1:
        return "An "
    return "A "

def EndCheck(message, Buffered):
    bufferSize = 0
    endingIt = True
    if Buffered:
        bufferSize = 3
    
    for endPart in ["end", "="]:
        if (endPart and ("''" or '""')) not in message[len(message) -
                                                       (9 + bufferSize):len(
                message) - bufferSize].lower():
            endingIt = False
    
    if endingIt:
        print(message[:len(message) - (9 + bufferSize)]
              + message[len(message) - bufferSize:], end = '')
    else:
        print(message)

def TwoTillSure(first, second, BOTinput):
    sureInput = GetInput(first, BOTinput)
    while not OkayWith("Are you Sure? "):
        sureInput = GetInput(second, BOTinput)
    return sureInput

TillSure = lambda message, BOTinput: TwoTillSure(message, message, BOTinput)


# 3 - PACING:

def CatchUp():
    if not AIMBOT:
        input("Type to Continue" + cursor)
    else:
        Pace("Type to Continue" + cursor + "* AIM BOT says: 'Blah blah' *")
        
def Pause(factor):
    try:
        # So Pause(0) is the quickest pause, Pause(3) longest
        time.sleep(Delays[factor])
    except IndexError:
        FoundError("An invalid pause factor was given")
        
def Pace(message):
    EndCheck(message, Buffered = False)
    Pause(1)
    
def OkayWith(message):
    if not AIMBOT:
        return input(message + cursor).lower() in ['y', "ye", "yeh",
                                                   "yes", "yea", "yeah",
                                                   "ok", "on", "okay", '1', '']
    else:
        Pace(message + cursor + "* AIM BOT says: 'Okay' *")
        return True
    
def SmartPace(message):
    EndCheck(message, Buffered = False)
    patienceFactor = 1 + float(round(len(message) / 75, 1))
    time.sleep(Delays[1] * patienceFactor)
    

# 4 - LISTING:

def Title(title):
    print("\n" + titleStart + str(title) + ': ' + titleEnd)
    Pause(3)
    print()

def List(optionsList, numbered):
    Pause(1)
    number = 0
    for option in optionsList:
        if numbered:
            number += 1
            DramaType("\t" + str(number) + ' ' + bullet + option + '\n')
        else:
            DramaType("\t" + bullet + option + '\n')
        time.sleep(Delays[0]/2)
    Pause(0)
    print()

def TitledList(title, optionsList, numbered):
    Pause(1)
    print("\n\t" + listStart + title + ': ' + listEnd)
    List(optionsList, numbered)

 
# 5 - AIMBOT:

def AssertDominance():
    if AIMBOT:
        DramaType("\t[ AIM BOT 'ON' ]")
        time.sleep(1)
        print()
        if Humanoid:
            print('\t', end = '')
            DotDot()
            print("I'm Hungry", end = '')
            DotDot()
            print()
            time.sleep(1)
    print()

def BOTslowIterate(Array, whenDone):
    global currentItem
    currentItem += 1
    if currentItem < len(Array):
        return Array[currentItem]
    else:
        currentItem = -1
        return whenDone

def GetInput(fromMessage, BOTinput):
    if AIMBOT:
        print(fromMessage + cursor + "* AIM BOT says: '" + str(BOTinput) +
              "' *")
        Pause(1)
        return BOTinput
    else:
        _input = input(fromMessage + cursor)
        Pause(1)
        return _input
    
def VaryBOTinputs(condition, whileFalse, whenTrue):
    if condition:
        return whenTrue
    else:
        return whileFalse


# 6 - UTILITIES:

def GoAway():
    print("Quiting in 3 secs...")
    time.sleep(2)
    for dot in range(3):
        print('. ')
        time.sleep(1)
    
    if not AIMBOT:
        print('_ ')
    else:
        input("err help... ")
    exit()

def Pure(phrase):
    if any(phrase):
        for removable in ['.', '?', ',', '#', '!', "'", '"', '\t', '\n', '  ']:
            while removable in phrase:
                if not removable == '  ':
                    phrase = phrase.replace(removable, '')
                else:
                    phrase = phrase.replace(removable, ' ')

        if len(phrase) > 1:
            while phrase[len(phrase) - 1] == ' ':
                phrase = phrase[:len(phrase) - 1]

    return phrase.lower()

def TryToRead(file):
    content = 0
    try:
        content = open(file, 'r').read()
    except:
        try:
            if file[len(file) - 4:] == ".txt":
                content = open(file[:len(file) - 4], 'r').read()
            else:
                content = open(file + ".txt", 'r').read()
        except:
            FoundError("Couldn't find the File")
    
    ErrorIf(not any(content), "The File is Empty")
    
    return list(filter(lambda line: any(line), content.split('\n')))

def Yessify(boolean):
    if boolean:
        return "Yes"
    return "No"

def SwitchUp(boolean):
    if boolean:
        return "On"
    return "Off"

def Release_Ready(MoreMods):
    Title("GitHub Release Check")
    # [["It's off", True]]
    
    JCmods = ["AIMBOT Off        : " + Yessify(not AIMBOT),
              "Humanoid Off      : " + Yessify(not Humanoid),
              "BOT Speed = 15    : " + Yessify(BOTspeed == 15),
              "DramaTyping On    : " + Yessify(DramaTyping),
              "Fresh Pages Off   : " + Yessify(not FreshPages),
              "Long Pause = 1.25 : " + Yessify(longPause == 1.25)]
    
    # Remove mods already reset...
    for ModList in [JCmods, MoreMods]:
        DoneOnes = []
        for mod in ModList:
            if mod[len(mod) - 3:].lower() == "yes":
                DoneOnes.append(mod)
        RemoveAll(DoneOnes, ModList)
    
    JCReady = not any(JCmods)
    MoreModsReady = not any(MoreMods)
    
    Pace("\t ...RELEASE READY: " + Yessify(JCReady and MoreModsReady).upper() +
         '!...\n')
    
    if not JCReady:
        print("\tJC.py Module Ready: " + Yessify(JCReady).upper() + "...\n")
        List(JCmods, True)
    
    if not MoreModsReady:
        print("\tBool Mods Reset: " + Yessify(MoreModsReady).upper() + "...\n")
        List(MoreMods, True)
    
    # input("Type to Continue" + cursor)
    CatchUp()
    WindowRefresh()
    
def ErrorIf(condition, message):
    if condition:
        Inform("Error: " + message + " end = ''")
        if not AIMBOT:
            input(cursor)
        else:
            Pace(cursor + "* AIM BOT says: 'Yeah yeah...' *")
        Pause(2)
        print()

        GoAway()
    
def InRange(lower, value, upper):
    if round(float(value)) < lower or round(float(value)) > upper:
        return False
    return True

def RemoveAll(these, FromHere):
    for item in these:
        FromHere.remove(item)
    return FromHere
    
def TheItem(where, currentItem, Array):
    try:
        if "Before" in where.lower().title():
            return Array[Array.index(currentItem) - 1]
        elif "Range" in where.lower().title():
            return InRange(0, currentItem, MaxIndex(Array))
        elif "Last" in where.lower().title():
            return Array.index(currentItem) == MaxIndex(Array)
        else:
            return Array[Array.index(currentItem) + 1]
    except IndexError:
        return ''
    
def OneArrayed(PossibleThings, InHere):
    for thing in PossibleThings:
        if thing in InHere:
            return True
    return False

def MenuResponse(title, Options, CarefulOptions = None):
    if any(title):
        TitledList(title, Options + CarefulOptions, 1)

    response = -1
    while not TheItem("In Range", response, Options + CarefulOptions):
        response = int(input('(Option number):- '))
        if response >= MaxIndex(Options):  # So in Careful Options
            if not OkayWith("Are you Sure?:- "):
                response = -1
    return response

def FinalChoice(Options):
    return MenuResponse("Final Options", Options.append("Quit the program."))

FoundError = lambda message: ErrorIf(True, message)