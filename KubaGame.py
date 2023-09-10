# Author: Jin Huang
# Description: Implementation of the KubaGame class. Kuba Game is a marble game that takes two players.
# Each player has 8 marbles (B,W) and the game has 13 neutral red marbles. If a player pushes off
# 7 red marbles or s/he pushes off all opponent's marbles, the player wins.
import copy

class KubaGame:
    """
    The class representing the Kuba game.
    """
    def __init__(self, *args):
        """
        Initializes game with two tuples (player name, color chosen) and initializes the board.
        """

        # unpack the input tuple to retreive player names and colors chosen.
        playerList = []
        for arg in args:
            playerList += list(arg)
        #print(playerList)
        self._nameA = playerList[0]
        self._nameB = playerList[2]
        self._colorA = playerList[1]
        self._colorB = playerList[3]

        # initialize necessary variables
        self._state = "UNFINISHED"              # game state initialized to unifinished
        self._current_turn = None
        self._nameA_red = 0                     # each player's captured red count
        self._nameB_red = 0
        self._is_valid = None                   # flag if a move is valid
        self._pushed_off = None                   # the marble that would be pushed off
        self._valid_direction =['B','F','L','R']      # a list of valid directions
        self._pre_opponent_move = []            # a list of copies of the board before opponent's moves.

        # board is a 7x7 2d list, each element of the list has a character that represents the color of the marble
        # "X" represents an empty space
        # initializes the board
        self._board = [
            ["W", "W", "X", "X", "X", "B", "B"],
            ["W", "W", "X", "R", "X", "B", "B"],
            ["X", "X", "R", "R", "R", "X", "X"],
            ["X", "R", "R", "R", "R", "R", "X"],
            ["X", "X", "R", "R", "R", "X", "X"],
            ["B", "B", "X", "R", "X", "W", "W"],
            ["B", "B", "X", "X", "X", "W", "W"]
        ]

    def get_pushed_off(self):
        """
        Returns the self._pushed_off marble
        """
        return self._pushed_off

    def get_pre_oppo_move(self):
        """Returns the self._pre_opponent_move list that contains
        the copies of the board before an opponent's move. """
        return self._pre_opponent_move

    def get_opponent(self, playerName):
        """
        Takes a player name and returns the opponent of the player.
        """
        if playerName == self._nameA:
            return self._nameB
        if playerName == self._nameB:
            return self._nameA
        else:
            return None

    def get_color(self, playerName):
        """
        Takes a player name and returns the color chosen by the player.
        """
        if playerName == self._nameA:
            return self._colorA
        if playerName == self._nameB:
            return self._colorB

    def get_name_from_color(self,color):
        """
        Takes a color and returns the name of the matching player.
        """
        if color == self.get_color(self._nameA):
            return self._nameA
        else:
            return self._nameB

    def get_A(self):
        """
        Returns the name and color info of player A
        """
        return self._nameA, self._colorA

    def get_B(self):
        """
        Returns the name and color info of player B
        """
        return self._nameB, self._colorB

    def get_current_turn(self):
        """
        Returns the player name whose turn it is to play the game.
        Returns None if called when no player has made the first move.
        """
        return self._current_turn

    def get_x(self, coordinates):
        """
        Takes coordinates and returns the x index (row).
        """
        row_index = coordinates[0]
        return row_index

    def get_y(self, coordinates):
        """
        Takes coordinates and returns the y index (row).
        """
        column_index = coordinates[1]
        return column_index

    def place_marble(self, row_index, column_index, marble):
        """
        Takes row index, column index, and marble (W,B,R).
        Assigns the marble to the corresponding board position.
        """
        self._board[row_index][column_index] = marble


    def count_consecutive(self, coordinates,direction):
        """
        Takes coordinates and a direction.
        Returns how many consecutive marbles are ahead of the marble at the coordinates
        along the given direction, i.e., stop counting if reaches a vacant square.
        """
        x_move = self.get_x(coordinates)
        y_move = self.get_y(coordinates)
        counter = 0

        if direction == "R":
            for index in range(y_move+1,7):
                if self.get_marble((x_move,index)) != "X":
                    counter += 1
                else:
                    return counter
        elif direction == "L":
            for index in reversed(range(0,y_move)):
                if self.get_marble((x_move,index)) != "X":
                    counter += 1
                else:
                    return counter
        elif direction == "B":
            for row in range(x_move+1,7):
                if self.get_marble((row,y_move)) != "X":
                    counter += 1
                else:
                    return counter
        elif direction == "F":
            for row in reversed(range(0,x_move)):
                if self.get_marble((row, y_move)) != "X":
                    counter += 1
                else:
                    return counter

    def push_right(self, coordinates, direction):
        """
        Takes coordinates and direction.
        Pushes the marble at the coordindates and the marbles ahead of it
        one index towards the right, i.e., rightward along the x axis.
        """
        x_move = self.get_x(coordinates)
        y_move = self.get_y(coordinates)
        counter = self.count_consecutive(coordinates,direction)

        # vacant square ahead of the move
        if counter is not None:
            #if self.get_marble((x_move,y_move+counter+1)) == "X":
            first_part = []
            second_part = []
            second_part_right_shift = []
            # Divide the first half (to shift) and the second half(unchanged)
            this_row = self._board[x_move]
            if y_move == 0:
                first_part = []
            elif y_move == 1:
                first_part.append(this_row[0])
            else:
                first_part = this_row[:y_move]
            #traverse this row until the first vacant square is found
            for index in range(y_move, 7):
                if this_row[index] != "X":
                    second_part.append(this_row[index])
                else:
                    break
            third_part_length = 7 - len(first_part) - len(second_part) - 1
            if third_part_length == 0:
                third_part = []
            else:
                third_part = this_row[-third_part_length:]

            for index in range(len(second_part)):
                this_marble = second_part.pop()
                second_part_right_shift.insert(0,this_marble)
            second_part_right_shift.insert(0,"X")
            # partially shifted
            this_row = first_part + second_part_right_shift + third_part
            # inplace
            self._board[x_move] = this_row

        # no vacant square ahead of the move
        elif counter is None:
            # save the marble to be pushed off
            self._pushed_off = self.get_marble((x_move, 6))

            this_row = []  # new shifted row
            old_row = self._board[x_move]               #the original row

            row_first_half = old_row[:y_move+1]         #keep the first part unchanged
            old_row = (old_row[-1:] + old_row[:-1])     #shift all elements to the right by one position
            row_second_half = old_row[y_move+1:]      #have the second half changed
            this_row = row_first_half + row_second_half

            self._board[x_move] = this_row            #put the shifted row in place
            self.place_marble(x_move, y_move, "X")  # replace the old position with empty square

            # place the new row back on the board
            self._board[x_move] = this_row

    def push_left(self, coordinates, direction):
        """
        Takes coordinates and direction.
        Pushes the marble at the coordindates and the marbles ahead of it
        one index towards the left, i.e., leftward along the x axis.
        """
        x_move = self.get_x(coordinates)
        y_move = self.get_y(coordinates)
        counter = self.count_consecutive(coordinates, direction)

        # vacant square ahead of the move
        if counter is not None:
            first_part = []
            second_part = []
            second_part_left_shift = []
            third_part = []
            this_row = self._board[x_move]
            if y_move == 6:
                third_part = []
            elif y_move == 5:
                third_part.append(this_row[6])
            else:
                third_part = this_row[y_move+1:]
            # traverse this row reversed until the first vacant square is found
            for index in reversed(range(y_move+1)):
                if this_row[index] != "X":
                    second_part.append(this_row[index])
                else:
                    break
            first_part_length = 7 - len(third_part) - len(second_part) - 1
            first_part = this_row[:first_part_length]

            for index in range(len(second_part)):
                this_marble = second_part.pop()
                second_part_left_shift.append(this_marble)
            second_part_left_shift.append("X")
            this_row = first_part + second_part_left_shift + third_part
            self._board[x_move] = this_row

        # no vacant square ahead of the move
        elif counter is None:
            # save the marble to be pushed off
            self._pushed_off = self.get_marble((x_move, 0))

            shifted_row = []  # new shifted row
            old_row = self._board[x_move]  # the original row

            row_second_half = old_row[y_move+1:]          #keep the second part unchanged
            old_row = old_row[1:] + old_row[:1]         #shift all elements to the left by one position
            row_first_half = old_row[:y_move+1]         #have the first part changed
            shifted_row = row_first_half + row_second_half

            self._board[x_move] = shifted_row  # put the shifted row in place

    def push_down(self, coordinates, direction):
        """
        Takes coordinates and direction.
        Pushes the marble at the coordindates and the marbles ahead of it
        one index downward, i.e., down along the y axis.
        """
        x_move = self.get_x(coordinates)
        y_move = self.get_y(coordinates)
        counter = self.count_consecutive(coordinates, direction)

        # vacant square ahead of the move
        if counter is not None:
            #unchanged top: row range(x_move)
            #changed: row range(x_move,x_move+counter+1)
            #unchanged bottomn:row_range...rest
            temp = []
            for row in range(x_move, x_move+counter+1):
                for column in range(0,7):
                    if column == y_move:
                        temp_marble = self.get_marble((row,column))
                        temp.insert(0, temp_marble)
            temp.append("X")
            # insert back
            for row in range(x_move, x_move+counter+2):
                to_insert = temp.pop()
                self.place_marble(row, y_move, to_insert)

        # no vacant square ahead of the move
        elif counter is None:
            # save the marble to be pushed off
            self._pushed_off = self.get_marble((6,y_move))

            # unchanged: row range(x_move)
            # changed: row range(x_move, 7)
            temp = []
            for row in range(x_move, 6):
                for column in range(0,7):
                    if column == y_move:            #along the moving axis
                        temp_marble = self.get_marble((row,column))
                        temp.insert(0, temp_marble)
            temp.append("X")
            # insert back
            for row in range(x_move,7):
                to_insert = temp.pop()
                self.place_marble(row,y_move,to_insert)

    def push_up(self, coordinates, direction):
        """
        Takes coordinates and direction.
        Pushes the marble at the coordindates and the marbles ahead of it
        one index upward, i.e., up along the y axis.
        """
        x_move = self.get_x(coordinates)
        y_move = self.get_y(coordinates)
        counter = self.count_consecutive(coordinates, direction)

        # vacant square ahead of the move
        if counter is not None:
            # unchanged bottomn: row range(x_move+1, 7)
            # changed: row range: (x_move-counter, x_move)
            # unchanged: row range: rest at top

            temp = []
            for row in reversed(range(x_move-counter, x_move+1)):
                for column in range(0,7):
                    if column == y_move:
                        temp_marble = self.get_marble((row,column))
                        temp.insert(0, temp_marble)
            temp.append("X")
            # insert back
            for row in reversed(range(x_move-counter-1,x_move+1)):
                to_insert = temp.pop()
                self.place_marble(row,y_move,to_insert)

        # no vacant square ahead of the move
        elif counter is None:
            # save the marble to be pushed off
            self._pushed_off = self.get_marble((0, y_move))

            # unchanged: row range(x_move+1,7)
            # changed: row range(x_move+1)
            temp = []
            for row in reversed(range(1,x_move+1)):
                for column in range(0,7):
                    if column == y_move:
                        temp_marble = self.get_marble((row, column))
                        temp.insert(0, temp_marble)
            temp.append("X")
            # insert back
            for row in reversed(range(0,x_move+1)):
                to_insert = temp.pop()
                self.place_marble(row, y_move, to_insert)

    def get_preceding_marble(self, coordinates, direction):
        """
        Takes coordinates and direction.
        Returns the marble that precedes the marble at the coordinates
        along the given direction.
        """
        x_move = self.get_x(coordinates)
        y_move = self.get_y(coordinates)

        if direction == "B":
            x_preceding = x_move - 1
            return self.get_marble((x_preceding, y_move))
        elif direction == "F":
            x_preceding = x_move + 1
            return self.get_marble((x_preceding, y_move))
        elif direction == "R":
            y_preceding = y_move - 1
            return self.get_marble((x_move, y_preceding))
        elif direction == "L":
            y_preceding = y_move + 1
            return self.get_marble((x_move, y_preceding))

    def validate_move(self, playerName, coordinates, direction):
        """
        Takes a player name, coordinates and direction.
        Checks the move against game rules.
        Returns is_valid as True if the move is valid.
        Returns is_valid as False if the move is invalid.
        """
        # check if the game has been won
        if self.get_winner() is not None:
            self._is_valid = False
            return self._is_valid

        # Check if the direction is valid
        if direction not in self._valid_direction or len(direction) == 0:
            self._is_valid = False
            return self._is_valid

        # Check if the player names are empty string
        if len(playerName) == 0:
            self._is_valid = False
            return self._is_valid

        # Check if the coordinates are valid
        # Empty string, less than 2 indices, or more than 2 indices
        if len(str(coordinates)) != 6:
            self._is_valid = False
            return self._is_valid
        else:
            if self.get_x(coordinates) not in range(0,7) or self.get_y(coordinates) not in range(0,7):
                self._is_valid = False
                return self._is_valid

        x_move = self.get_x(coordinates)
        y_move = self.get_y(coordinates)

        # Check if the game has been won
        if self._state != "UNFINISHED":
            self._is_valid = False
            return self._is_valid

        # Check if this is the player's turn
        if self.get_current_turn() is None:
            self._is_valid = True
        elif playerName != self.get_current_turn():
            self._is_valid = False
            return self._is_valid

        # Check if this is the player's marble
        if self.get_color(playerName) != self.get_marble(coordinates):
            self._is_valid = False
            return self._is_valid

        # Check edge of the board preceding or empty space preceding
        # edge of the board
        # if x_move in [0,6] or y_move in [0,6]:

        if direction == 'F':
            if x_move == 0:
                self._is_valid = False
                return self._is_valid
            elif x_move == 6:
                return self._is_valid
            elif self.get_preceding_marble(coordinates, direction) != "X":
                self._is_valid = False
            return self._is_valid

        elif direction == 'B':
            if x_move == 6:
                self._is_valid = False
                return self._is_valid
            elif x_move == 0:
                return self._is_valid
            elif self.get_preceding_marble(coordinates, direction) != "X":
                self._is_valid = False
            return self._is_valid

        elif direction == 'L':
            if y_move == 0:
                self._is_valid = False
                return self._is_valid
            elif y_move == 6:
                return self._is_valid
            elif self.get_preceding_marble(coordinates, direction) != "X":
                self._is_valid = False
            return self._is_valid
        elif direction == 'R':
            if y_move == 6:
                self._is_valid = False
                return self._is_valid
            elif y_move == 0:
                return self._is_valid
            elif self.get_preceding_marble(coordinates, direction) != "X":
                self._is_valid = False
            return self._is_valid


    def make_move(self, playerName, coordinates, direction):
        """
        Takes playerName, coordinates, and direction.
        Calls validate_move to validate the player's move.
        Calls one of the four make move functions to make the player's move.
        Returns True if the move is valid and successufl.
        Returns False if the move is invalid or unsuccessful.
        Updates marble count, turn, game state.
        """
        # Copy the board of before opponent move for later comparison
        pre_opp_move = copy.deepcopy(self._board)
        self._pre_opponent_move.insert(0, pre_opp_move)

        # validate moves
        # call self.validate_move
        # check if is_valid is True
        self.validate_move(playerName, coordinates, direction)
        if self._is_valid is False:
            self._is_valid = None  # reset is_valid
            self._pushed_off = None # reset _pushed_off
            #print("False")
            return False

        else:
            marble_count_before = self.get_marble_count()
            red_count_before = marble_count_before[2]

            if direction == "R":  # right
                self.push_right(coordinates,direction)
            elif direction == "L": # left
                self.push_left(coordinates,direction)
            elif direction == "B":  # downward
                self.push_down(coordinates,direction)
            elif direction == "F":  # upward
                self.push_up(coordinates, direction)

            # verify if a player pushes off his own marble
            if self._pushed_off is not None:
                player_marble = self.get_color(playerName)
                if self._pushed_off == player_marble:
                # if the marble to be pushed is the same as the playerName's marble,
                # invalid move, undo this move, return False
                    self._board = self._pre_opponent_move[0]  # go back to pre-this-move, i.e. post-last-move
                    self._pre_opponent_move.pop(0)  # pre-this-move board is no longer needed
                    #print("Invalid move, cannot push off your own marble.")
                    self._pushed_off = None  # reset _pushed_off
                    return False
            else:
                self._pushed_off = None  # reset _pushed_off

            #compare board
            if len(self._pre_opponent_move) > 1 and self._board == self._pre_opponent_move[1]:
                    #print("Invalid, undo move")
                    self._board = self._pre_opponent_move[0]   # go back to pre-this-move, i.e. post-last-move
                    self._pre_opponent_move.pop(0)             # pre-this-move board is no longer needed
                    return False
            elif len(self._pre_opponent_move) > 1 and self._board != self._pre_opponent_move[1]:
            # self._board != pre-last-move
                self._pre_opponent_move.pop()           # this move is verified in terms of undo moves

            # if red captured
            marble_count_after = self.get_marble_count()
            red_count_after = marble_count_after[2]
            if red_count_after != red_count_before:
                if playerName == self._nameA:
                    self._nameA_red += 1
                elif playerName == self._nameB:
                    self._nameB_red += 1

            # finishing up the game
            # mark turn
            next_turn = self.get_opponent(playerName)
            self._current_turn = next_turn
            # reset is_valid
            self._is_valid = None
            self._pushed_off = None  # reset _pushed_off

            # Check win
            if self.get_winner() is not None:
                #print(self.get_winner())
                self.get_winner()
            # print("True")
            return True

    def get_winner(self):
        """
        Returns the name of the winning player.
        Returns None if no winner yet.
        Checks if a player has won.
        If so, change game_state to "FINISHED". If not, no update.
        """
        marble_count = self.get_marble_count()
        if self._nameA_red == 7:  # PlayerA captures 7 red, won
            self._state = "FINISHED"
            #print(self._state)
            return self._nameA
        elif self._nameB_red == 7:  # PlayerB captures 7 red, won
            self._state = "FINISHED"
            #print(self._state)
            return self._nameB
        elif marble_count[0] == 0:  # White marbles are 0, black marbles won
            self._state = "FINISHED"
            #print(self._state)
            return self.get_name_from_color('B')
        elif marble_count[1] == 0:  # Black marbles are 0, white marbles won
            self._state = "FINISHED"
            #print(self._state)
            return self.get_name_from_color('W')
        else:
            return None

    def get_captured(self, playerName):
        """
        Takes a playerName. Returns how many Red marbles have been captured by this player.
        Returns 0 if no Red marble captured.
        """
        if playerName == self._nameA:
            return self._nameA_red
        elif playerName == self._nameB:
            return self._nameB_red

    def get_marble(self, coordinates):
        """
        Takes coordinates.
        Returns the marble that is present at the coordinates position.
        Returns 'X' if no marble at the location.
        """
        x_index = self.get_x(coordinates)
        y_index = self.get_y(coordinates)
        return self._board[x_index][y_index]

    def get_marble_count(self):
        """
        Returns the number of marbles currently on the board,
        in the following order: White, Black, and Red as tuple (W,B,R).
        """
        count_W = 0
        count_B = 0
        count_R = 0

        for row in range(0,7):
            for column in range(0,7):
                if self.get_marble((row,column)) == "W":
                    count_W += 1
                elif self.get_marble((row, column)) == "B":
                    count_B += 1
                elif self.get_marble((row, column)) == "R":
                    count_R += 1
        return (count_W, count_B, count_R)
