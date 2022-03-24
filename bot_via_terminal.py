#!/usr/bin/env python3
"""Script to interact with the bot via the terminal"""

from tic_tac_toe_bot import TicTacToeBot, BoardStatus, Difficulty
import enum

class State(enum.Enum):
    COMPUTER_TURN = 0
    HUMAN_TURN = 1

def main() -> None:
    bot = TicTacToeBot(Difficulty.HARD)
    state = State.HUMAN_TURN
    while bot.is_end_of_game() == BoardStatus.UNFINISHED:
        if state == State.HUMAN_TURN:
            bot.print_board()
            row = int(input("Row: ")) - 1
            col = int(input("Col: ")) - 1
            print("")

            if bot.play_opponent(row, col):
                state = State.COMPUTER_TURN

        elif state == State.COMPUTER_TURN:
            bot.play()
            state = State.HUMAN_TURN

    print(bot.is_end_of_game().name)

if __name__ == '__main__':
    main()