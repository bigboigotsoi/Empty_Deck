from time import sleep

# Customize these variables
titleStart = " -- "
titleEnd = " -- "

listStart = "~ "
listEnd = " ~"

bullet = '- '
cursor = ":- "

dramatypeSpeed = 0.75

Aim_Bot = True
Humanoid = False
A_User = not Aim_Bot
Aim_Bot_Can_Dip = False

Impatient = False
FreshPages = False
DramaTyping = True

# Sorting out the JC Timings
if Humanoid or not Aim_Bot:
    howSpedUp = 1
else:
    howSpedUp = 10

# Define the largest pause time, then the
# smaller ones will be auto-generated.
if not Impatient:
    # Change this from 1.5 if you want 
    longPause = 1.5
else:
    longPause = 0
    
currentItem = -1

Delays = []
for count in range(4):
    if longPause:
        # They decrease in size exponentially
        Delays.insert(0, round(longPause / (2 ** count * howSpedUp), 2))
    else:
        Delays = [0, 0, 0, 0]

# Small helpful/nice looking lambdas
Any = lambda thing: thing or type(thing) in [list, str] and not len(thing) == 0
Capitalize = lambda word: word[0].upper() + word[1: ]
MaxIndex = lambda Array: len(Array) - 1
Quote = lambda phrase: "'" + phrase + "'"

# JC FUNCTIONS: In Categories of...

# 1 - PRESENTATION:

def FreshPage():
    if FreshPages:
        print('\n' * 38)
        
def Inform(message):
    EndCheck("\n* " + message + " * ", Buffered = True)

def IsBusy(theThing):
    print()
    DramaticElipses(1)
    print(str(theThing), end = '')
    DramaticElipses(1)
    Pause(1)
    print()
    print()

def DramaType(message, speed):
    # Uses a constant time frame, so long
    # messages are forced to be more rapid.
    if DramaTyping:
        for character in message:
            print(character, end = '')
            sleep(Delays[1]/(len(message) * speed))
    else:
        print(message)
        
DramaticElipses = lambda speed: Spam('.', 3, 0.25 * speed/howSpedUp, False)


# 2 - MESSAGING:

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
        
def Spam(theSpam, spamCount, spamPeriod, Down):
    Pause(1)
    for spamDone in range(spamCount):
        if not Down:
            print(theSpam, end = '')
        else:
            print(theSpam)
        if not Impatient:
            sleep(spamPeriod / (howSpedUp * spamCount))

def SayThingsUntil(firstMessage, secondMessage, botAnswer):
    _okayInput = GetInput(firstMessage, botAnswer)
    while A_User and not OkayWith("Is this Okay? "):
        _okayInput = GetInput(secondMessage, botAnswer)
    return _okayInput

SayUntil = lambda message, botAnswer: SayThingsUntil(message, message, botAnswer)


# 3 - PACING:

def Stop():
    if not Aim_Bot:
        input(cursor)
    else:
        Pace(cursor + "* AIM BOT says: 'Yeah yeah...' *")

def CatchUp():
    if not Aim_Bot:
        input("Type to Continue" + cursor)
    else:
        Pace("Type to Continue" + cursor + "* AIM BOT says: 'yes' *")
        
def Pace(message):
    EndCheck(message, Buffered = False)
    Pause(2)
    
def Pause(howLong):
    try:
        # So Pause(0) is the quickest pause, Pause(3) longest
        sleep(Delays[howLong])
    except IndexError:
        FoundError("An invalid pause duration was given")
        
def OkayWith(message):
    if not Aim_Bot:
        return input(message + cursor).lower() in ['y', "ye", "yeh", "yes", "yea", "yeah", "ok", "okay", '1', '']
    else:
        Pace(message + cursor + "* AIM BOT says: 'yes' *")
        return True
    
def SmartPace(message):
    EndCheck(message, Buffered = False)
    patienceFactor = 1 + float(round(len(message) / 75, 1))
    sleep(Delays[1] * patienceFactor)

def GoAwayIn(seconds, Down):
    Stop()
    Pause(2)
    print()
    DramaticElipses(1)
    print("Closing in " + str(seconds) + " seconds ", end = '')
    if not Down:
        Pause(1)
        Spam('. ', 2, seconds / howSpedUp, False)
        print(' _ ', end = '')
    else:
        DramaticElipses(1)
        Pause(1)
        print()
        Spam('. ', 2, seconds / howSpedUp, True)
        print('- ', end = '')
    
    if not Aim_Bot or Aim_Bot and Aim_Bot_Can_Dip:
        exit()
    else:
        input("er, help...")
        exit()

GoAway = lambda: GoAwayIn(2, True)


# 4 - LISTING:

def Title(title):
    print("\n" + titleStart + str(title) + titleEnd)
    Pause(3)
    print()

def List(optionsList, numbered):
    Pause(1)
    number = 0
    for option in optionsList:
        if numbered:
            number += 1
            DramaType("\t" + str(number) + ' ' + bullet + option + '\n', dramatypeSpeed)
        else:
            DramaType("\t" + bullet + option + '\n', dramatypeSpeed)
        sleep(Delays[0]/2)
    Pause(0)
    print()

def TitledList(title, optionsList, numbered):
    Pause(1)
    print("\n\t" + listStart + title + ':' + listEnd)
    List(optionsList, numbered)

 
# 5 - AIM_BOT:

def AssertDominance():
    if Aim_Bot:
        DramaType("\t[ AIM BOT 'ON' ]", dramatypeSpeed)
        sleep(1)
        print()
        if Humanoid:
            print('\t', end = '')
            DramaticElipses(1)
            print("I'm Hungry", end = '')
            DramaticElipses(1)
            print()
            sleep(1)
    else:
        print("\tHello User...")
        sleep(1)
    print()

def BotSlowIterate(Array, whenDone):
    global currentItem
    currentItem += 1
    if currentItem < len(Array):
        return Array[currentItem]
    else:
        currentItem = -1
        return whenDone

def GetInput(fromMessage, botAnswer):
    if Aim_Bot:
        print(fromMessage + cursor + "* AIM BOT says: '" + str(botAnswer) +
              "' *")
        Pause(1)
        return botAnswer
    else:
        _input = input(fromMessage + cursor)
        Pause(1)
        return _input
    
def VaryBotAnswers(condition, whileFalse, whenTrue):
    if condition:
        return whenTrue
    else:
        return whileFalse


# 6 - UTILITIES:

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
    
    if Any(content):
        return content
    else:
        FoundError("The File is Empty")
    
def Yessify(boolean):
    if boolean:
        return "Yes"
    return "No"

def JC_Release_Ready():
    Title("GitHub Release Check")
    
    print("\t ...RELEASE READY: " + Yessify(not (Aim_Bot or Impatient or
                                                 FreshPages or Aim_Bot_Can_Dip)
                                            and howSpedUp == 1).upper() + '...\n')
    
    List(["Aim Bot Off       : " + Yessify(not Aim_Bot),
          "Humanoid Off      : " + Yessify(not Humanoid),
          "Impatience Off    : " + Yessify(not Impatient),
          "DramaTyping Off   : " + Yessify(not DramaTyping),
          "Fresh Pages Off   : " + Yessify(not FreshPages),
          "Bot Can Dip Off   : " + Yessify(not Aim_Bot_Can_Dip),
          "Speed Factor == 1 : " + Yessify(howSpedUp == 1)], True)
    
    input("Type to Continue" + cursor)
    
def FoundError(message):
    Inform("Error: " + message + " end = ''")
    GoAway()
    
def NextItem(Array, currentItem):
    try:
        return Array[Array.index(currentItem) + 1]
    except IndexError:
        return ''
    
def PreviousItem(Array, currentItem):
    try:
        return Array[Array.index(currentItem) - 1]
    except IndexError:
        return ''
    
def AThingsArrayed(ArrayOfThings, Array):
    for thing in ArrayOfThings:
        if thing in Array:
            return True
    return False