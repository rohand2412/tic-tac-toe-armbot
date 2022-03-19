#!/usr/bin/env python3
"""This script plays tictactoe against you"""

import numpy as np
import enum

BOARD_LEN = 3
LATERAL_SUM_MAT = np.ones(3)

def findBestMove(board: np.ndarray) -> tuple:
    bestVal = -10
    bestMove = None
    for i in range(len(board)):
        for j in range(len(board[i])):
            if not board[i][j]:
                board[i][j] = 1
                val = minimax(board, 0, False)
                board[i][j] = 0
                if val >= bestVal:
                    bestVal = val
                    bestMove = (i, j)
    return bestMove

def minimax(board: np.ndarray, depth: int, maximize: bool) -> int:
    endGameVal = endOfGame(board)
    if endGameVal != BoardStatus.UNFINISHED:
        if endGameVal == BoardStatus.COMPUTER_WINS:
            return endGameVal.value * 10 - depth
        elif endGameVal == BoardStatus.PLAYER_WINS:
            return endGameVal.value * 10 + depth

    draw = True
    if maximize:
        bestVal = BoardStatus.PLAYER_WINS.value * 10
        for i in range(len(board)):
            for j in range(len(board[i])):
                if not board[i][j]:
                    draw = False
                    board[i][j] = 1
                    bestVal = max(bestVal, minimax(board, depth+1, not maximize))
                    board[i][j] = 0
    else:
        bestVal = BoardStatus.COMPUTER_WINS.value * 10
        for i in range(len(board)):
            for j in range(len(board[i])):
                if not board[i][j]:
                    draw = False
                    board[i][j] = -1
                    bestVal = min(bestVal, minimax(board, depth+1, not maximize))
                    board[i][j] = 0

    if draw:
        return BoardStatus.DRAW.value
    else:
        return bestVal

class BoardStatus(enum.Enum):
    UNFINISHED = 2
    COMPUTER_WINS = 1
    PLAYER_WINS = -1
    DRAW = 0

def endOfGame(board: np.ndarray) -> BoardStatus:
    row_sum_mat = np.matmul(board, LATERAL_SUM_MAT)
    col_sum_mat = np.matmul(board.transpose(), LATERAL_SUM_MAT)
    top_left_diag_sum = board[0][0] + board[1][1] + board[2][2]
    top_right_diag_sum = board[0][2] + board[1][1] + board[2][0]

    if (np.amax(row_sum_mat) >= BOARD_LEN * 1
        or np.amax(col_sum_mat) >= BOARD_LEN * 1
        or top_left_diag_sum >= BOARD_LEN * 1
        or top_right_diag_sum >= BOARD_LEN * 1):
        return BoardStatus.COMPUTER_WINS
    elif (np.amin(row_sum_mat) <= BOARD_LEN * -1
          or np.amin(col_sum_mat) <= BOARD_LEN * -1
          or top_left_diag_sum <= BOARD_LEN * -1
          or top_right_diag_sum <= BOARD_LEN * -1):
        return BoardStatus.PLAYER_WINS
    else:
        draw = True
        for i in range(len(board)):
            for j in range(len(board[i])):
                if not board[i][j]:
                    draw = False
        if draw:
            return BoardStatus.DRAW
        else:
            return BoardStatus.UNFINISHED

def printBoard(board: np.ndarray) -> None:
    for i in range(len(board) - 1):
        for j in range(len(board[i]) - 1):
            print(str(-board[i][j]) + " | ", end="")
        print(-board[i][len(board[i]) - 1])
        print("---------")
    for j in range(len(board[len(board) - 1]) - 1):
        print(str(-board[len(board) - 1][j]) + " | ", end="")
    print(-board[len(board) - 1][len(board[len(board) - 1]) - 1])


def main() -> None:
    board = np.zeros((BOARD_LEN, BOARD_LEN), dtype=int)
    computerTurn = False
    flipPlayer = True
    boardStatus = endOfGame(board)
    while boardStatus == BoardStatus.UNFINISHED:
        if computerTurn:
            print("")
            move = findBestMove(board)
            board[move] = 1
        else:
            printBoard(board)
            row = int(input("Row: ")) - 1
            col = int(input("Col: ")) - 1
            if not board[row][col]:
                board[row][col] = -1
            else:
                flipPlayer = False
        if flipPlayer:
            computerTurn = not computerTurn
        else:
            flipPlayer = True
            print("")
        boardStatus = endOfGame(board)
    print(boardStatus.name)

if __name__ == '__main__':
    main()