from time import sleep

Yesses = ['y', "ye", "yeh", "yes", "yea", "yeah", "ok", "okay", '1', '']
Delays = []

# You can customize these variables
titleStart = " -- "
titleEnd = " -- "

listStart = "~ "
listEnd = " ~"

bullet = '- '
cursor = ":- "

Aim_Bot = False
A_User = not Aim_Bot
Aim_Bot_Can_Dip = False
Humanoid = False
Impatient = False
WelcomingUser = True

# Leave the rest below alone...
if Humanoid or not Aim_Bot:
    howSpedUp = 1
else:
    howSpedUp = 10

# Give the largest pause time, then the
# smaller ones will be auto-generated.
# Set it to 0 to have no pauses.
if not Impatient:
    longPauseSize = 1.5
else:
    longPauseSize = 0

longPause = longPauseSize / howSpedUp

for count in range(4):
    if longPauseSize == 0:
        Delays = [0, 0, 0, 0]
    else:
        # They decrease in size exponentially
        Delays.insert(0, round(longPause / 2 ** count, 2))

averagePaceTime = Delays[1] / howSpedUp

# Helpful Lambdas
Any = lambda thing: thing or type(thing) == list and not len(thing) == 0
Validate = lambda data, match: data == match
Validate = lambda data, criteriaList: data in criteriaList
Capitalize = lambda word: word[0].upper() + word[1: ]

def AssertDominance():
    if Aim_Bot:
        print("\t> AIM BOT ON <")
        sleep(1)
        print()
        if Humanoid:
            IsBusy("I'm Hungry")
            sleep(1)
            print()
    else:
        if WelcomingUser:
            print("\tHello User...")
            sleep(1)
            print()
    
def OkayWith(message):
    if not Aim_Bot:
        return Validate(input(message + cursor).lower(),Yesses)
    else:
        Pace(message + cursor + "* AIM BOT says: 'yes' *")
        return True

def CatchUp():
    if not Aim_Bot:
        input("Type to Continue" + cursor)
    else:
        Pace("Type to Continue" + cursor + "* AIM BOT says: 'yes' *")

def SayStuffUntil(firstMessage, secondMessage, botAnswer):
    _okayInput = GetInput(firstMessage, botAnswer)
    while A_User and not OkayWith("Is this Okay? "):
        _okayInput = GetInput(secondMessage, botAnswer)
    return _okayInput

SayUntil = lambda message, botAnswer: SayStuffUntil(message, message, botAnswer)

def Pause(howLong):
    try:
        # So Pause(0) is the quickest pause, Pause(3) longest
        sleep(Delays[howLong])
    except IndexError:
        FoundError("An invalid pause duration was given")
        
def EndCheck(message, Buffered):
    bufferSize = 0
    if Buffered:
        bufferSize = 3
        
    if message[len(message) - (9 + bufferSize) :
    len(message) - bufferSize] == " end = ''":
        
        print(message[:len(message) - (9 + bufferSize)]
              + message[len(message) - bufferSize:], end = '')
    else:
        print(message)

def Pace(message):
    EndCheck(message, Buffered = False)
    Pause(2)

def Stop():
    if not Aim_Bot:
        input(cursor)
    else:
        Pace(cursor + "* AIM BOT says: 'Yeah yeah...' *")

def SmartPace(message):
    EndCheck(message, Buffered = False)
    patienceFactor = 1 + float(round(len(message) / 75, 1))
    sleep(averagePaceTime * patienceFactor)

def Inform(message):
    EndCheck("\n* " + message + " * ", Buffered = True)
    
def IsBusy(theThing):
    Pace("\n..." + str(theThing) + "...")
    print()

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
            print("\t" + str(number) + ' ' + bullet + "'" + option + "'")
        else:
            print("\t" + bullet + "'" + option + "'")
        Pause(0)
    Pause(0)
    print()

def TitledList(title, optionsList, numbered):
    Pause(1)
    print("\n\t" + listStart + title + ':' + listEnd)
    List(optionsList, numbered)

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
        
def CountDown(totalTime, dotsToPrint):
    Pause(2)
    for doneDots in range(dotsToPrint):
        print('.')
        sleep(totalTime / (howSpedUp * dotsToPrint))
        
def GoAwayIn(seconds, dotsToPrint):
    Stop()
    Pause(2)
    print("\n...Closing in " + str(seconds) + " seconds...")
    CountDown(seconds, dotsToPrint)
    print('- ', end = '')
    if not Aim_Bot or Aim_Bot and Aim_Bot_Can_Dip:
        exit()
    else:
        input("er, help...")
        exit()
        
GoAway = lambda: GoAwayIn(2, 2)

def FoundError(message):
    Inform("Error: " + message)
    GoAway()


