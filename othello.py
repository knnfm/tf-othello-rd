#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@author: Keisuke Ueda
http://qiita.com/keisuke1111/items/53353896a957136b1d7e
refactoring by @shiracamus
'''

import time
import random
import copy

from debug_log import DebugLog

class Othello:
    def __init__(self):
        self.board = None
        self.player1 = None
        self.player2 = None
        self.turn = 0
        self.hand1 = None
        self.hand2 = None
        self.log = DebugLog()

    # ---------------------------------------------------------
    # 学習モデルと対戦のオセロ　-----------------------------------
    # ---------------------------------------------------------

    # 機械学習用のAPIたち
    # 学習用に1手1手プレイしていくスタイルの初期化
    def test_start_play(self):
        self.board = Board()
        self.player1 = User(BLACK, "PC")
        self.player2 = AI(WHITE, "AI")
        self.turn = 0
        self.hand1 = None
        self.hand2 = None

    def test_player_play(self):
        self.hand1 = self.player1.play(self.board)
        if self.hand1 == "ok":
            self.log.verbose(self.board)
            hand_str = "(" + str(x) + ", " + str(y) + ")"
            self.log.verbose("%sの手: %s" % (self.player1.name, hand_str))
        return self.hand1

    def test_ai_play(self, x, y):
        DebugLog.verbose(str(x) + ":" + str(y))
        self.hand1 = self.player2.play(self.board, x, y)
        if self.hand1 == "ok":
            self.log.verbose(self.board)
            hand_str = "(" + str(x) + ", " + str(y) + ")"
            self.log.verbose("%sの手: %s" % (self.player1.name, hand_str))
        return self.hand1


    # ---------------------------------------------------------
    # 学習用のオセロ　---------------------------------------------
    # ---------------------------------------------------------


    # 機械学習用のAPIたち
    # 学習用に1手1手プレイしていくスタイルの初期化
    def learning_start_play(self):
        self.board = Board()
        self.player1 = AI(BLACK, "AI")
        self.player2 = Computer(WHITE, "PC")
        self.turn = 0
        self.hand1 = None
        self.hand2 = None

    # 学習用に1手1手プレイしていくスタイルの
    def learning_play(self, x, y):
        self.hand1 = self.player1.play(self.board, x, y)
        if self.hand1 == "ok":
            self.log.verbose(self.board)
            hand_str = "(" + str(x) + ", " + str(y) + ")"
            self.log.verbose("%sの手: %s" % (self.player1.name, hand_str))
        return self.hand1

    def learning_next(self):
        self.turn += 1
        # print("TURN = %s" % self.turn)

        # print(self.board)
        self.hand2 = self.player2.play(self.board)
        # print("%sの手: %s" % (self.player2.name, self.hand2))

    def learning_observe(self):
        return self.board, self.reward, self.is_playable()

    def is_playable(self):
        return self.board.is_playable() and not self.hand1 == self.hand2 == "pass"

    def get_board_square(self):
        return self.board.square

    # ---------------------------------------------------------
    # 通常のオセロ　---------------------------------------------
    # ---------------------------------------------------------

    def play(self):
        start_time = time.time()
        board = Board()
        player1 = computer = Computer(BLACK, "PC")
        player2 = user = User(WHITE, "あなた")
        # player1 = user = User(BLACK, "あなた")
        # player2 = computer = Computer(WHITE, "PC")

        turn = 0
        hand1 = hand2 = None
        while board.is_playable() and not hand1 == hand2 == "pass":
            turn += 1
            print("TURN = %s" % turn)

            print(board)
            hand1 = player1.play(board)
            print("%sの手: %s" % (player1.name, hand1))

            print(board)
            hand2 = player2.play(board)
            print("%sの手: %s" % (player2.name, hand2))

        self.show_result(board)

        end_time = time.time()
        print("試合時間:" + str(end_time - start_time))

    def show_result(self, board):
        # print("------------------RESULT-------------------")  # 結果発表
        # print(board)
        user_stones = board.count(self.player1.stone)
        computer_stones = board.count(self.player2.stone)
        # print(str(user_stones) + " : " + str(computer_stones))
        # print("Computer: %s" % computer_stones)
        # print("You: %s" % user_stones)
        if computer_stones > user_stones:
            print("LOSE " + str(user_stones) + " : " + str(computer_stones))
        elif computer_stones < user_stones:
            print("WINN " + str(user_stones) + " : " + str(computer_stones))
        else:
            print("DRAW " + str(user_stones) + " : " + str(computer_stones))


class Stone(str):
    pass


BLACK = Stone("●")
WHITE = Stone("○")
BLANK = Stone("×")
OPPONENT = {BLACK: WHITE, WHITE: BLACK}


class Board:
    SIZE = 8
    DIRECTIONS_XY = ((-1, -1), (+0, -1), (+1, -1),
                     (-1, +0), (+1, +0),
                     (-1, +1), (+0, +1), (+1, +1))

    def __init__(self):
        size = self.SIZE
        center = size // 2
        square = [[BLANK for y in range(size)] for x in range(size)]  # 最初の盤面を定義
        square[center - 1][center - 1:center + 1] = [WHITE, BLACK]
        square[center + 0][center - 1:center + 1] = [BLACK, WHITE]
        self.square = square

    def __str__(self):
        log = "\ 0 1 2 3 4 5 6 7\n"

        row_count = 0
        for row in self.square:
            log += str(row_count) + " "
            for column in row:
                log += column + " "
            log += "\n"
            row_count += 1

        return log

    def __getitem__(self, x):
        return self.square[x]

    def is_playable(self):
        return any(col != BLANK
                   for row in self.square
                   for col in row)

    def count(self, stone):  # 石が何個あるかを返す関数
        return sum(col == stone  # True is 1, False is 0
                   for row in self.square
                   for col in row)

    def put(self, x, y, stone):  # y,xは置く石の座標、stoneにはWHITEかBLACKが入る。
        self[x][y] = stone

        for dx, dy in Board.DIRECTIONS_XY:
            n = self.count_reversible(x, y, dx, dy, stone)
            for i in range(1, n + 1):
                self[x + i * dx][y + i * dy] = stone

    def count_reversible(self, x, y, dx, dy, stone):
        size = self.SIZE
        for n in range(size):
            x += dx
            y += dy
            if not (0 <= x < size and 0 <= y < size):
                return 0
            if self[x][y] == BLANK:
                return 0
            if self[x][y] == stone:
                return n
        return 0

    def is_available(self, x, y, stone):
        if self[x][y] != BLANK:
            return False
        return any(self.count_reversible(x, y, dx, dy, stone) > 0
                   for dx, dy in self.DIRECTIONS_XY)

    def availables(self, stone):  # 打てる場所の探索
        return [(x, y)
                for x in range(self.SIZE)
                for y in range(self.SIZE)
                if self.is_available(x, y, stone)]


class Player:  # abstract class

    def __init__(self, stone, name):
        self.stone = stone
        self.name = name

    def play(self, board):
        availables = board.availables(self.stone)
        if not availables:
            return "pass"
        return self.think(board, availables)


class AI:
    def __init__(self, stone, name):
        self.stone = stone
        self.name = name

    def play(self, board, x, y):
        availables = board.availables(self.stone)
        if not availables:
            return "pass"

        # Catchballに盤面を渡して考えさせる
        DebugLog.info("打てる場所(Y, X): " + str(availables))
        if (x, y) in availables:
            board.put(x, y, self.stone)
            return "ok"
        else:
            return "ng"


class Computer(Player):

    def think(self, board, availables):
        starttime = time.time()
        DebugLog.info(availables)
        # print("thinking……")
        own = self.stone
        opponent = OPPONENT[own]
        evaluations, x, y = AlphaBeta(board, availables, own, opponent)
        # print(evaluations)
        board.put(x, y, self.stone)
        endtime = time.time()
        interval = endtime - starttime
        # print("%s秒" % interval)  # 計算時間を表示
        return x, y


class User(Player):
    def think(self, board, availables):
        while True:
            DebugLog.info("打てる場所(Y, X): " + str(availables))  # 内部のx,yと表示のX,Yが逆なので注意
            try:
                print("eq:\"2 3\"")
                line = input("Y X or quit: ")
                print("line is " + line)
            except:
                print("エラー")
                print("強制終了")
                exit(1)
            if line == "quit" or line == "exit":
                print("放棄終了")
                exit(1)
            try:
                x, y = map(int, line.split())
                if (x, y) in availables:
                    board.put(x, y, self.stone)
                    return x, y
                else:
                    print("そこには置けません")
            except:
                print("意味不明")


## --------------------------------------------
## 以下、テスト用のコンピュータ思考
## --------------------------------------------

def AlphaBeta(board, availables, own, opponent):  # AlphaBeta法で探索する
    # evaluations = AlphaBeta_evaluate1(board, availables, own, opponent)
    # if len(evaluations) == 0:
    #     maximum_evaluation_index = availables.index(max(availables))
    #     x, y = availables[maximum_evaluation_index]
    #     return evaluations, x, y
    # else:
    #     maximum_evaluation_index = evaluations.index(max(evaluations))
    #     x, y = availables[maximum_evaluation_index]
    #     return evaluations, x, y
    maximum_evaluation_index = availables.index(max(availables))
    x, y = availables[maximum_evaluation_index]
    return [], x, y


def AlphaBeta_evaluate1(board, availables, own, opponent):
    def pruning2(max_evaluations3):
        return len(evaluations1) > 0 and max(evaluations1) >= max_evaluations3

    print "evalute1 " + str(availables)
    evaluations1 = []
    for x, y in availables:
        board1 = copy.deepcopy(board)
        board1.put(x, y, own)
        evaluations2 = AlphaBeta_evaluate2(board1, own, opponent, pruning2)
        if len(evaluations2) > 0:
            evaluations1 += [min(evaluations2)]
    print "evaluations1 " + str(evaluations1)
    return evaluations1


def AlphaBeta_evaluate2(board, own, opponent, pruning):
    def pruning3(min_evaluations4):
        return len(evaluations2) > 0 and min(evaluations2) <= min_evaluations4

    evaluations2 = []
    for x, y in board.availables(opponent):
        board2 = copy.deepcopy(board)
        board2.put(x, y, opponent)
        evaluations3 = AlphaBeta_evaluate3(board2, own, opponent, pruning3)
        if len(evaluations3) > 0:
            max_evaluations3 = max(evaluations3)
            evaluations2 += [max_evaluations3]
            if pruning(max_evaluations3):
                break
    print "evaluations2 " + str(evaluations2)
    return evaluations2


def AlphaBeta_evaluate3(board, own, opponent, pruning):
    def pruning4(max_evaluations5):
        return len(evaluations3) > 0 and max(evaluations3) >= max_evaluations5

    evaluations3 = []
    for x, y in board.availables(own):
        board3 = copy.deepcopy(board)
        board3.put(x, y, own)
        evaluations4 = AlphaBeta_evaluate4(board3, own, opponent, pruning4)
        if len(evaluations4) > 0:
            min_evaluations4 = min(evaluations4)
            evaluations3 += [min_evaluations4]
            if pruning(min_evaluations4):
                break
    print "evaluations3 " + str(evaluations3)
    return evaluations3


def AlphaBeta_evaluate4(board, own, opponent, pruning):
    def pruning5(evaluation5):
        return len(evaluations4) > 0 and min(evaluations4) <= evaluation5

    evaluations4 = []
    for x, y in board.availables(opponent):
        board4 = copy.deepcopy(board)
        board4.put(x, y, opponent)
        evaluations5 = AlphaBeta_evaluate5(board4, own, opponent, pruning5)
        if len(evaluations5) > 0:
            max_evaluation5 = max(evaluations5)
            evaluations4 += [max_evaluation5]
            if pruning(max_evaluation5):
                break
    print "evaluations4 " + str(evaluations4)
    return evaluations4


def AlphaBeta_evaluate5(board, own, opponent, pruning):
    evaluations5 = []
    for x, y in board.availables(own):
        board5 = copy.deepcopy(board)
        board5.put(x, y, own)
        ev_own = evaluate(board5, own)
        ev_opponent = evaluate(board5, opponent)
        evaluation = ev_own - ev_opponent
        evaluations5 += [evaluation]
        if pruning(evaluation):
            break
    print "evaluations5 " + str(evaluations5)
    return evaluations5


# pp = [45,-11,-16,4,-1,2,-1,-3,-1,0]
EVALUATION_BOARD = (  # どのマスに石があったら何点かを表す評価ボード
    (45, -11, 4, -1, -1, 4, -11, 45),
    (-11, -16, -1, -3, -3, -1, -16, -11),
    (4, -1, 2, -1, -1, 2, -1, 4),
    (-1, -3, -1, 0, 0, -1, -3, -1),
    (-1, -3, -1, 0, 0, -1, -3, -1),
    (4, -1, 2, -1, -1, 2, -1, 4),
    (-11, -16, -1, -3, -3, -1, -16, -11),
    (45, -11, 4, -1, -1, 4, -11, 45))


def evaluate(board, stone):  # 任意の盤面のどちらかの石の評価値を計算する
    bp = 0
    for x in range(board.SIZE):
        for y in range(board.SIZE):
            if board[x][y] == BLANK:
                pass
            elif board[x][y] == stone:
                bp += EVALUATION_BOARD[x][y] * random.random() * 3
            else:
                bp -= EVALUATION_BOARD[x][y] * random.random() * 3

    p = confirm_stone(board, stone)
    q = confirm_stone(board, OPPONENT[stone])
    fs = ((p - q) + random.random() * 3) * 11

    b = board.availables(stone)
    cn = (len(b) + random.random() * 2) * 10

    evaluation = bp * 2 + fs * 5 + cn * 1
    return evaluation


def confirm_stone(board, stone):  # 確定石の数を数える
    forward = range(0, board.SIZE)
    backward = range(board.SIZE - 1, -1, -1)
    corners = ((+0, +0, forward, forward),
               (+0, -1, forward, backward),
               (-1, +0, backward, forward),
               (-1, -1, backward, backward))
    confirm = 0
    for x, y, rangex, rangey in corners:
        for ix in rangex:
            if board[ix][y] != stone:
                break
            confirm += 1
        for iy in rangey:
            if board[x][iy] != stone:
                break
            confirm += 1
    return confirm


if __name__ == '__main__':
    Othello().play()
