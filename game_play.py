import random
import time
import serial

import models
import chess

STATE_START = 0
STATE_PLAY = 1
STATE_WAIT = 2
STATE_END = 3

state = STATE_START
turn = 0
curr_player = None
curr_row = 0
curr_col = 0
winner = None

if __name__ == "__main__":
    p1 = models.Player("white")
    p2 = models.Player("black")

    chess.start()

    while(1):
        if (state == STATE_START):
            # button press?
            # print("Wizard's Chess!")
            # chess.speakText("Wizard's chess!")
            # print("Player 1, what's your name?")
            # chess.speakText("Player 1, what's your name?")
            # p1.setName(chess.prompt(state))
            # print("Ok! Player 1's name is " + p1.name + ".")
            # chess.speakText("Ok! Player 1's name is " + p1.name)
            # print("Player 2, what's your name?")
            # chess.speakText("Player 2, what's your name?")
            # p2.setName(chess.prompt(state))
            # print("Ok! Player 2's name is " + p2.name)
            # chess.speakText("Ok! Player 2's name is " + p2.name + ".")
            print("GAME START!")
            chess.speakText("Game start!")
            state = STATE_PLAY

        if (state == STATE_PLAY):
            if (turn % 2 == 0):
                curr_player = p1
            else:
                curr_player = p2

            state = STATE_WAIT

        while (state == STATE_WAIT):
            # print("What's your move? [<from-location> (pause) <piece> (pause) <to-location]")
            # chess.speakText("What's your move?")
            # word = chess.prompt(state)
            # text = chess.parseText(word.lower())
            #
            # chess.ifTakePiece(text[0], text[1], text[2])
            # curr_row = chess.alphabet[text[2][0]]
            # curr_col = int(text[2][1])
            #
            # data = chess.toMove(text[0], text[1], text[2])
            if turn == 0:
                data = ''.join(str(x) for x in [0,0,3,0,0,0,0])
            elif turn == 1:
                data = ''.join(str(x) for x in [5,-2,-3,0,0,0,0])


            # data = ''.join(str(x) for x in [1, 2, 1, 0, 0])

            # send data
            ArduinoSerial = serial.Serial('/dev/cu.usbserial-1450', 9600)
            time.sleep(2)
            print("sending data")
            ArduinoSerial.write(data.encode())
            # for i in data:
            #     command = str.encode(str(i))
            #     print(command)
            #     ArduinoSerial.write(command)

            print("Moving your piece.")
            chess.speakText("Moving your piece.")
            time.sleep(3)
            print("Moving your piece..")
            time.sleep(3)
            print("Moving your piece...")
            time.sleep(4)

            # update
            turn += 1
            # chess.grid[curr_row][curr_col] = models.Location(text[1],  curr_player.color)

            if (len(p1.lostPieces) == 16):
                winner = p2
                state = STATE_END
            elif (len(p2.lostPieces) == 16):
                winner = p1
                state = STATE_END
            else:
                state = STATE_PLAY
                print("NEXT TURN!")
                chess.speakText("Next turn!")
                time.sleep(2)


            # print grid
            grid = chess.grid
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

        if (state == STATE_END):
            print('GAME OVER! ' + winner.name + ' wins!')
            break
