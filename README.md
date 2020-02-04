# Wizard's Chess
Our Wizards’ Chess magically moves chess pieces through voice command 

Just like the chess board in Harry Potter, our chess game listens for speech-recognized chess commands and moves the pieces accordingly. 
The board is set up “double decker” style, with a mechanical arm underneath and a chessboard on top of it. 
In our implementation, we used Python to store all the game details and then send data to the Arduino for movement implementation.


We use two continuous rotation servos for moving pieces up and down the board and one micro servo with a magnet to attach to the piece being moved


Arduino -> 
Listens for serial input from Python
Uses servos to move both horizontally and vertically, accordingly

Python -> 
Stores 2D array of board coordinate system and pieces
Prompts user and listens for speech with adequate error checking and responds to user’s inputs (both visually and audibly)
Sends data about movement to Arduino via serial port


Our game allows visually or physically impaired to play a game of chess without having to actually move pieces. 

The computer prompts and re-prompts based on user input and audibly calls out the state of the game.


