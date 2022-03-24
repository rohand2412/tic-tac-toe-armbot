#!/usr/bin/env python3
"""Tic Tac Toe Bot Library"""

import numpy as np
import enum
import random

class BoardStatus(enum.Enum):
    UNFINISHED = 2
    COMPUTER_WINS = 1
    PLAYER_WINS = -1
    DRAW = 0

class Difficulty(enum.Enum):
    EASY = 0
    MEDIUM = 1
    HARD = 2

class TicTacToeBot:
    """Encapsulates all tictactoe logic and data"""

    BOARD_LEN = 3
    _LATERAL_SUM_MAT = np.ones(3)
    XO_TABLE = {-1: "X", 0: " ", 1: "O"}

    def __init__(self, difficulty: Difficulty):
        self._difficulty = difficulty
        self._turnsPlayed = 0
        self._board = np.zeros((TicTacToeBot.BOARD_LEN, TicTacToeBot.BOARD_LEN), dtype=int)

    def play(self) -> None:
        """Updates the board with the computer's move"""
        self._board[self._find_best_move()] = 1
        self._turnsPlayed += 1

    def play_opponent(self, row: int, col: int) -> bool:
        """Updates the board with the opponent's move"""
        if not self._board[row][col]:
            self._board[row][col] = -1
            return True
        else:
            return False

    def is_end_of_game(self) -> BoardStatus:
        """Checks if the game is over and who won"""
        row_sum_mat = np.matmul(self._board, TicTacToeBot._LATERAL_SUM_MAT)
        col_sum_mat = np.matmul(self._board.transpose(), TicTacToeBot._LATERAL_SUM_MAT)
        top_left_diag_sum = self._board[0][0] + self._board[1][1] + self._board[2][2]
        top_right_diag_sum = self._board[0][2] + self._board[1][1] + self._board[2][0]

        if (np.amax(row_sum_mat) >= TicTacToeBot.BOARD_LEN * 1
            or np.amax(col_sum_mat) >= TicTacToeBot.BOARD_LEN * 1
            or top_left_diag_sum >= TicTacToeBot.BOARD_LEN * 1
            or top_right_diag_sum >= TicTacToeBot.BOARD_LEN * 1):
            return BoardStatus.COMPUTER_WINS
        elif (np.amin(row_sum_mat) <= TicTacToeBot.BOARD_LEN * -1
            or np.amin(col_sum_mat) <= TicTacToeBot.BOARD_LEN * -1
            or top_left_diag_sum <= TicTacToeBot.BOARD_LEN * -1
            or top_right_diag_sum <= TicTacToeBot.BOARD_LEN * -1):
            return BoardStatus.PLAYER_WINS
        else:
            draw = True
            for i in range(len(self._board)):
                for j in range(len(self._board[i])):
                    if not self._board[i][j]:
                        draw = False
            if draw:
                return BoardStatus.DRAW
            else:
                return BoardStatus.UNFINISHED

    def print_board(self) -> None:
        """Displays the board"""
        for i in range(len(self._board) - 1):
            for j in range(len(self._board[i]) - 1):
                print(TicTacToeBot.XO_TABLE[self._board[i][j]] + " | ", end="")
            print(TicTacToeBot.XO_TABLE[self._board[i][len(self._board[i]) - 1]])
            print("---------")
        for j in range(len(self._board[len(self._board) - 1]) - 1):
            print(TicTacToeBot.XO_TABLE[self._board[len(self._board) - 1][j]] + " | ", end="")
        print(TicTacToeBot.XO_TABLE[self._board[len(self._board) - 1][len(self._board[len(self._board) - 1]) - 1]])

    def _find_best_move(self) -> tuple:
        """Finds the best move for the computer"""
        if self._difficulty == Difficulty.EASY:
            return self._find_best_move_easy()
        elif self._difficulty == Difficulty.MEDIUM:
            if self._turnsPlayed % 2 == 0:
                return self._find_best_move_easy()
            else:
                return self._find_best_move_hard()
        elif self._difficulty == Difficulty.HARD:
            return self._find_best_move_hard()

    def _find_best_move_easy(self) -> tuple:
        """Finds the best move for the computer on HARD difficulty"""
        movesVisited = 0
        bestMove = None
        for i in range(len(self._board)):
            for j in range(len(self._board[i])):
                if not self._board[i][j]:
                    movesVisited += 1
                    if random.random() < 1/movesVisited:
                        bestMove = (i, j)
        return bestMove

    def _find_best_move_hard(self) -> tuple:
        """Finds the best move for the computer on HARD difficulty"""
        bestVal = -10
        bestMove = None
        for i in range(len(self._board)):
            for j in range(len(self._board[i])):
                if not self._board[i][j]:
                    self._board[i][j] = 1
                    val = self._minimax(0, False)
                    self._board[i][j] = 0
                    if val >= bestVal:
                        bestVal = val
                        bestMove = (i, j)
        return bestMove

    def _minimax(self, depth: int, maximize: bool) -> int:
        """Minimax algorithm that determines the best move"""
        endGameVal = self.is_end_of_game()
        if endGameVal != BoardStatus.UNFINISHED:
            if endGameVal == BoardStatus.COMPUTER_WINS:
                return endGameVal.value * 10 - depth
            elif endGameVal == BoardStatus.PLAYER_WINS:
                return endGameVal.value * 10 + depth

        draw = True
        if maximize:
            bestVal = BoardStatus.PLAYER_WINS.value * 10
            for i in range(len(self._board)):
                for j in range(len(self._board[i])):
                    if not self._board[i][j]:
                        draw = False
                        self._board[i][j] = 1
                        bestVal = max(bestVal, self._minimax(depth+1, not maximize))
                        self._board[i][j] = 0
        else:
            bestVal = BoardStatus.COMPUTER_WINS.value * 10
            for i in range(len(self._board)):
                for j in range(len(self._board[i])):
                    if not self._board[i][j]:
                        draw = False
                        self._board[i][j] = -1
                        bestVal = min(bestVal, self._minimax(depth+1, not maximize))
                        self._board[i][j] = 0

        if draw:
            return BoardStatus.DRAW.value
        else:
            return bestVal
