#!/usr/bin/env python3
"""Tic Tac Toe Bot Library"""

import numpy as np
import enum

class BoardStatus(enum.Enum):
    UNFINISHED = 2
    COMPUTER_WINS = 1
    PLAYER_WINS = -1
    DRAW = 0

class TicTacToeBot:
    """Encapsulates all tictactoe logic and data"""

    def __init__(self):
        self.BOARD_LEN = 3
        self._LATERAL_SUM_MAT = np.ones(3)
        self._board = np.zeros((self.BOARD_LEN, self.BOARD_LEN), dtype=int)

    def play(self) -> None:
        self._board[self._find_best_move()] = 1

    def play_opponent(self, row: int, col: int) -> bool:
        if not self._board[row][col]:
            self._board[row][col] = -1
            return True
        else:
            return False

    def is_end_of_game(self) -> BoardStatus:
        row_sum_mat = np.matmul(self._board, self._LATERAL_SUM_MAT)
        col_sum_mat = np.matmul(self._board.transpose(), self._LATERAL_SUM_MAT)
        top_left_diag_sum = self._board[0][0] + self._board[1][1] + self._board[2][2]
        top_right_diag_sum = self._board[0][2] + self._board[1][1] + self._board[2][0]

        if (np.amax(row_sum_mat) >= self.BOARD_LEN * 1
            or np.amax(col_sum_mat) >= self.BOARD_LEN * 1
            or top_left_diag_sum >= self.BOARD_LEN * 1
            or top_right_diag_sum >= self.BOARD_LEN * 1):
            return BoardStatus.COMPUTER_WINS
        elif (np.amin(row_sum_mat) <= self.BOARD_LEN * -1
            or np.amin(col_sum_mat) <= self.BOARD_LEN * -1
            or top_left_diag_sum <= self.BOARD_LEN * -1
            or top_right_diag_sum <= self.BOARD_LEN * -1):
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
        for i in range(len(self._board) - 1):
            for j in range(len(self._board[i]) - 1):
                print(str(-self._board[i][j]) + " | ", end="")
            print(-self._board[i][len(self._board[i]) - 1])
            print("---------")
        for j in range(len(self._board[len(self._board) - 1]) - 1):
            print(str(-self._board[len(self._board) - 1][j]) + " | ", end="")
        print(-self._board[len(self._board) - 1][len(self._board[len(self._board) - 1]) - 1])

    def _find_best_move(self) -> tuple:
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
