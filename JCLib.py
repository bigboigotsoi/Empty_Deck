import time

# Customize these variables
import JCLib as JCLib

bullet = '- '
cursor = ':' + bullet
listStart = listEnd = "~ "
titleStart = titleEnd = " -- "

FreshPages = False
DramaTyping = True

# Creating JC Timings:

# Define the largest pause, and
# Smaller ones will be auto-generated.
longPause = 0.5



# JC FUNCTIONS: In Categories of...

# 1 - PRESENTATION:

def Wipe_CLI(always = False):
    if FreshPages or always:
        print('\n' * 38)

def Separate_CLI(prelines=0, newlines=1):
    print("\n"*prelines + "_  "*15 + "\n"*newlines)
        
def Notify(message, prelines=1, newlines=1, tabs=0):
    print('\n'*prelines + '\t'*tabs + '*', message, '* ', end='')
    Pause(2)
    print('\n' * newlines, end='')

def Doing(something, pace=1, prelines=1, newlines=1, tabs=0):
    if prelines:
        print('\n' * prelines)

    print('\t'*tabs, end='')
    # DramaType("...")
    print(str(something), end='')
    DramaType("...", newlines=newlines)
    Pause(pace)

def An(control_number):
    if control_number == 1:
        return "An "
    return "A "

def DramaType_How(message, duration, pace=1, prelines=0, newlines=1):  # By default, make next text start on next line, end = '' is newlines = 0.
    if prelines:
        print('\n' * prelines)

    if DramaTyping:
        for character in message:
            print(character, end = '')
            time.sleep(duration / len(message))
        if newlines:
            print('\n'*newlines, end='')
    else:
        print(message, end='')

    Pause(pace)
    if newlines and not DramaTyping:
        print('\n'*newlines, end='')

def Sure_Response(message):
    _input = Get_Input(message)
    while not Okay_With("Are you sure?"):
        Sure_Response(message)
    return _input



# 2 - PACING:

Delays = [0, 0, 0, 0]
if longPause:
    for count in range(4):
        # Decrease in size exponentially
        Delays[len(Delays)-(count+1)] = longPause / 2.5 ** count
        # Or linearly
        # Delays[len(Delays)-(count+1)] = longPause / (count+1)
    del Delays[4:]
dramaDuration = Delays[1]

DramaType = lambda message, pace=1, duration=dramaDuration, prelines=0, newlines=1: DramaType_How(message, duration=dramaDuration,
                                                                                                   pace=pace, prelines=prelines,
                                                                                                   newlines=newlines)

Prompt = lambda: input("Type to Continue" + cursor)
        
def Pause(factor):
    if factor >= 0:
        try:
            # So Pause(0) is the quickest pause, Pause(3) longest
            time.sleep(Delays[factor])
        except IndexError:
            Error("Invalid pause factor")
        
def Pace(message, pace=1, prelines=0, newlines=1):
    print("\n"*prelines + message + "\n"*newlines)
    Pause(pace)


    
# 3 - LISTING:

def Title(title, pace=3, prelines=1, newlines=1, tabs=0):
    print('\n'*prelines + '\t'*tabs, titleStart + str(title) + ':', titleEnd + '\n'*newlines)
    Pause(pace)

def List(options_list, pace=0, numbered=False, prelines=1, newlines=2, tabs=0):
    number = 0
    Pause(1)

    if prelines:
        print('\n' * prelines)

    for option in options_list:
        if numbered:
            number += 1
            DramaType('\t'*tabs + str(number) + '  ' + option, newlines=0)
        else:
            DramaType('\t'*tabs + bullet + ' ' + option, newlines=0)
        time.sleep(Delays[0]/2)

        if not JCLib.The_Item("Is The Last", option, options_list):
            print()
        elif newlines:
            print('\n' * newlines)
    Pause(pace)

def Titled_List(title, options_list, numbered=True, pace=0, prelines=1, newlines=1, tabs=0):
    Pause(1)
    print('\n'*prelines + '\t'*tabs + listStart + title + ':', listEnd)
    List(options_list, numbered=numbered, pace=pace, prelines=0, newlines=1, tabs=tabs)

def Valid_Index(index, array):
    if index > -1 and index < len(array) - 1:
        return True
    return False

def Remove_All(these, FromHere):
    for item in these:
        FromHere.remove(item)
    return FromHere

def The_Item(where, currentItem, Array):
    try:
        if "Before" in where.lower().title():
            return Array[Array.index(currentItem) - 1]
        elif "Range" in where.lower().title():
            return In_On_Bounds(0, currentItem, len(Array) - 1)
        elif "Last" in where.lower().title():
            return Array.index(currentItem) == len(Array) - 1
        else:
            return Array[Array.index(currentItem) + 1]
    except IndexError:
        return ''

def One_Listed(PossibleThings, InHere):
    for thing in PossibleThings:
        if thing in InHere:
            return True
    return False

def Menu_Response(title, Options, CarefulOptions = [], prelines=1, newlines=0, tabs=0):
    if any(title):
        Titled_List(title, Options + CarefulOptions, numbered=True, prelines=prelines, newlines=1, tabs=tabs)
    else:
        List(Options, numbered=True, prelines=prelines, newlines=1, tabs=tabs)
    
    response = -1
    while not In_On_Bounds(1, response, len(Options + CarefulOptions)):
        response = Get_Input()
        if not any(response):
            response = -1
        else:
            response = int(response)
            if response > len(Options) and In_On_Bounds(0, response, len(Options + CarefulOptions)):  # So in Careful Options
                if not Okay_With("Are you Sure?:- "):
                    response = -1
    return response

def Final_Menu(Options):
    return Menu_Response("Final Options", Options.append("Quit the program."))



# 4 - UTILITIES:

Error = lambda message: Error_When(True, message)

Okay_With = lambda message: input(message + cursor).lower() in ['y', "ye",
                                                                "yeh",
                                                                "yes", "yea",
                                                                "yeah",
                                                                "ok", "on",
                                                                "okay", '1', '']

Commanded = lambda command, text: Stripped(command) in Stripped(text)

Matched = lambda sentence, goal_sentence: \
    all(word in Stripped(sentence).split() for word in Stripped(goal_sentence).split())

def End():
    print("Quiting in 3 secs...")
    time.sleep(2)
    for dot in range(3):
        print('. ')
        time.sleep(1)
    print('_ ')
    exit()

def Try_Read(file):
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
            Error("Couldn't find the File")
    
    Error_When(not any(content), "The File is Empty")
    
    return list(filter(lambda line: any(line), content.split('\n')))

def Stripped(phrase):
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

def Yessify(boolean):
    if boolean:
        return "Yes"
    return "No"

def Switch_Up(boolean):
    if boolean:
        return "On"
    return "Off"

def Release_Ready(MoreMods):
    Title("GitHub Release Check", pace=-1)
    # [["It's off", True]]

    JCmods = ["DramaTyping On    : " + Yessify(DramaTyping).lower(),
              "Fresh Pages Off   : " + Yessify(not FreshPages).lower(),
              "Long Pause = 1.25 : " + Yessify(longPause == 1.25).lower()]

    # Remove mods already reset...
    for ModList in [JCmods, MoreMods]:
        DoneOnes = []
        for mod in ModList:
            if mod[len(mod) - 3:].lower() == "yes":
                DoneOnes.append(mod)
        Remove_All(DoneOnes, ModList)

    JCReady = not any(JCmods)
    MoreModsReady = not any(MoreMods)

    Pace("\t ...RELEASE READY: " + Yessify(JCReady and MoreModsReady).upper() +
         '!...\n')
    Pause(2)

    if not JCReady:
        print("   JC.py Module Ready: " + Yessify(JCReady).upper() + "...")
        List(JCmods, prelines=0)


    if not MoreModsReady:
        Pause(2)
        print("   Bool Mods Reset: " + Yessify(MoreModsReady).upper() + "...")
        List(MoreMods, prelines=0)

    Pause(2)
    Prompt()
    Wipe_CLI(always=True)

def Get_Input(fromMessage='', pace=1):
    _input = input(fromMessage + cursor)
    Pause(pace)
    return _input

def Error_When(condition, message):
    if condition:
        Notify("Error: " + message, newlines=0)
        input(cursor)
        Pause(2)
        print()
        End()
    
def In_On_Bounds(lower, value, upper):
    if lower <= value and value <= upper:
        return True
    return False

