import random
import time

import speech_recognition as sr
from gtts import gTTS
import os
import pyttsx3

import models
import game_play

grid = []
alphabet = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
piece_names = ['king', 'queen', 'bishop', 'knight', 'rook', 'pop']

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


def speakText(command):

    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


def start():
    for i in range(8):
        innergrid = []
        for j in range(8):
            innergrid.append(None)
        grid.append(innergrid)

    for j in range (8):
        grid[1][j] = models.Location("pop", "white")
        grid[6][j] = models.Location("pop", "black")

    grid[0][0] = models.Location("rook", "white")
    grid[0][7] = models.Location("rook", "white")
    grid[7][0] = models.Location("rook", "black")
    grid[7][7] = models.Location("rook", "black")

    grid[0][1] = models.Location("knight", "white")
    grid[0][6] = models.Location("knight", "white")
    grid[7][1] = models.Location("knight", "black")
    grid[7][6] = models.Location("knight", "black")

    grid[0][2] = models.Location("bishop", "white")
    grid[0][5] = models.Location("bishop", "white")
    grid[7][2] = models.Location("bishop", "black")
    grid[7][5] = models.Location("bishop", "black")

    grid[0][3] = models.Location("queen", "white")
    grid[0][4] = models.Location("king", "white")
    grid[7][4] = models.Location("queen", "black")
    grid[7][3] = models.Location("king", "black")

    text = '['
    for row in grid:
        text += '['
        for loc in row:
            if loc is not None:
                text += str(loc.color) + str(loc.piece) + ' '
            else:
                text += 'None' + ' '
        text += ']'
    text += ']'
    print('grid is ' + text)


def parseText(word):
    fromLoc = word[:word.index(' ')]
    word = word[word.index(' ')+1:]
    piece = word[:word.index(' ')]
    toLoc = word[word.index(' ')+1:]
    return [fromLoc, piece, toLoc]


def check_format(text):
    if (text.count(' ') != 2):
        return False

    try:
        temp = parseText(text.lower())

        print("one")
        one = temp[0][0] in alphabet
        print("two")
        two = type(int(temp[0][1])) == int
        print("three")
        three = temp[1] in piece_names
        print("four")
        four = temp[2][0] in alphabet
        print("five")
        five = type(int(temp[2][1])) == int

        if (one and two and three and four and five):
            print("if true")
            return True
        else:
            print("if false")
            return False

    except:
        print("except false")
        return False


def check_valid_move(text):
    temp = parseText(text.lower())
    piece = temp[1]
    data = toMove(temp[0], temp[1], temp[2])

    print("data: " + str(data))

    fmr = data[0]
    fmc = data[1]
    smr = data[2]
    smc = data[3]

    firstMoveRow = abs(data[0])
    firstMoveCol = abs(data[1])
    secondMoveRow = abs(data[2])
    secondMoveCol = abs(data[3])

    start_row = alphabet[temp[0][0]]
    start_col = int(temp[0][1:])

    # if (grid[start_row][start_col] is None):
    #     return False
    #
    # # check that piece is in spot
    # if (grid[start_row][start_col].piece != piece):
    #     print("check piece in spot")
    #     return False
    #
    # # if out of bounds
    # if (0 > firstMoveRow + secondMoveRow > 7 or 0 > firstMoveCol + secondMoveCol > 7):
    #     print("piece out of bounds")
    #     return False

    # if correct move for correct piece

    if (piece == 'king'):
        # can't move more than 1 space
        print("king")
        if (secondMoveRow + secondMoveCol > 2):
            print("false")
            return False

    elif (piece == 'queen'):
        # can't move in L's
        if (secondMoveRow > 0 and secondMoveCol > 0 and secondMoveRow != secondMoveCol):
            return False
        elif (secondMoveRow > 0 and secondMoveCol != 0):
            return False
        elif (secondMoveCol > 0 and secondMoveRow != 0):
            return False

    elif (piece == 'bishop'):
        # must be diagonals
        if (secondMoveRow != secondMoveCol):
            return False

    elif (piece == 'knight'):
        pass

    elif (piece == 'rook'):
        # must be horizontal or vertical
        if (secondMoveRow > 0 and secondMoveCol > 0):
            return False

    elif (piece == 'pop'):
        print("pop")
        try:
            front = grid[game_play.curr_row+1][game_play.curr_col]
        except:
            front = None

        try:
            front_left = grid[game_play.curr_row+1][game_play.curr_col-1]
        except:
            front_left = None

        try:
            front_right = grid[game_play.curr_row+1][game_play.curr_col+1]
        except:
            front_right = None

        # # not at starting position
        # if (int(temp[0][1]) != 1 or int(temp[0][1]) != 6):
        #     print("not at start")
        #     if (smr == 1 and smc == 1 and front_right is None):
        #         return False
        #     elif (smr == 1 and smc == -1 and front_left is None):
        #         return False
        #     elif (smr == 1 and smc == 0 and front is not None):
        #         return False
        #     elif (secondMoveRow > 1 or secondMoveCol > 1):
        #         return False
        #
        # # at starting position
        # else:
        #     print("at start")
        #     if (secondMoveRow > 2 or secondMoveCol > 1):
        #         return False
        #     elif (secondMoveRow == 2 and secondMoveCol != 0):
        #         return False
        #     elif (smr == 1 and smc == 0 and front is not None):
        #         return False
        #     elif (smr == 1 and smr == 1 and front_right is None):
        #         return False
        #     elif (smr == 1 and smc == -1 and front_left is None):
        #         return False

    print("valid true")
    return True


def prompt(state):
    PROMPT_LIMIT = 5

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    correct = False

    while(not correct):
        good_format = False
        valid_move = False
        while (not good_format or not valid_move):
            # ask for user input
            for j in range(PROMPT_LIMIT):
                print('Wait 4 seconds then speak!')
                speakText("Wait 4 seconds then speak!")
                guess = recognize_speech_from_mic(recognizer, microphone)
                if guess["transcription"]:
                    good_format = True
                    valid_move = True
                    break
                if not guess["success"]:
                    good_format = True
                    valid_move = True
                    break
                print("I didn't catch that. What did you say?")
                speakText("I didn't catch that. What did you say?")
            print(guess["transcription"])
            if guess["error"]:
                print("ERROR: {}".format(guess["error"]))
                break

            if (state != 0):
                good_format = check_format(guess["transcription"])
                if (good_format):
                    valid_move = check_valid_move(guess["transcription"])

            if (not good_format):
                print("Must be of valid format. Try again.")
                speakText("Must be of valid format. Try again.")
            elif (not valid_move):
                print("Must be a valid move. Try again.")
                speakText("Must be a valid move. Try again.")

        # ask if correct
        print("Did you say {}? [Yes/No]".format(guess["transcription"]))
        speakText('did you say ' + guess["transcription"] + '?')

        for j in range(PROMPT_LIMIT):
            print("Wait 4 seconds then speak!")
            speakText("Wait 4 seconds then speak!")
            check = recognize_speech_from_mic(recognizer, microphone)
            if check["transcription"]:
                break
            if not check["success"]:
                break
            print("I didn't catch that. What did you say?")
            speakText("I didn't catch that. What did you say?")

        if check["error"]:
            print("ERROR: {}".format(check["error"]))
            break

        correct = check["transcription"].lower() == 'yes'
        if (not correct):
            print("You said no. Ok, let's try again!")
            speakText("You said no. Ok, let's try again!")

    return guess["transcription"]


def ifTakePiece(fromLoc, piece, toLoc):
    destCol = alphabet[toLoc[0]]
    destRow = int(toLoc[1:])

    if (grid[destRow][destCol] != None):
        curr_player.takenPieces.append(grid[destRow][destCol].piece)

        if curr_player == p1:
            game_play.p2.lostPieces.append(grid[destRow][destCol].piece)
            game_play.p2.activePieces.remove(grid[destRow][destCol].piece)
        else:
            game_play.p1.lostPieces.append(grid[destRow][destCol].piece)
            game_play.p1.activePieces.remove(grid[destRow][destCol].piece)


def toMove(fromLoc, piece, toLoc):
    """
    fromLoc:    format <letter><number>     ex: "a0"
    piece:      format <name>               ex: "king"
    toLoc:      format <letter><number>     ex: "a0"
    """
    startCol = alphabet[fromLoc[0]]
    startRow = int(fromLoc[1])
    destCol = alphabet[toLoc[0]]
    destRow = int(toLoc[1])

    firstMoveRow = startRow - game_play.curr_row
    firstMoveCol = startCol - game_play.curr_col

    secondMoveRow = destRow-startRow
    secondMoveCol = destCol-startCol

    # removing old piece position
    grid[startRow][startCol] = None

    # assuming we move first by row then by column
    pathObstacles = []
    for i in range (startRow, destRow):
        if grid[i][startCol] is not None:
            pathObstacles.append(1)
        else:
            pathObstacles.append(0)

    for j in range (startCol, destCol):
        if grid[destRow][j] is not None:
            pathObstacles.append(1)
        else:
            pathObstacles.append(0)

    return [firstMoveRow, firstMoveCol, secondMoveRow, secondMoveCol] + pathObstacles
