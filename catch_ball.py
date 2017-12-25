#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ゲームと評価を繋ぐところ

import os
import random
import numpy as np

from othello import Othello


class CatchBall:
    def __init__(self):
        self.board = None
        self.othello = None
        self.reward = 0
        self.name = os.path.splitext(os.path.basename(__file__))[0]
        self.enable_actions = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63)

    # 現在の盤面を取得
    def observe(self):
        full_board = np.zeros((8, 8))

        row_count = 0
        for row in self.othello.get_board_square():
            column_count = 0
            for column in row:
                if column == "●":  # 黒
                    full_board[row_count][column_count] = 1
                elif column == "○":  # 白
                    full_board[row_count][column_count] = -1

                column_count += 1

            row_count += 1
        return np.array(full_board, dtype=np.int32)


    def observe_ng(self, action):
        x = int(action % 8)
        y = int(action / 8)
        full_board = np.zeros((8, 8))

        row_count = 0
        for row in self.othello.get_board_square():
            log = ""

            column_count = 0
            for column in row:
                if column == "●":  # 黒
                    full_board[row_count][column_count] = 1
                    log += "●"
                elif column == "○":  # 白
                    full_board[row_count][column_count] = -1
                    log += "○"
                elif column_count == y and row_count == x:
                    full_board[row_count][column_count] = -1
                    log += "○"
                else:
                    log += "×"

                column_count += 1

            row_count += 1
            # print log
        

        return np.array(full_board, dtype=np.int32)

    # 評価を取得
    def get_stone_reward(self):
        return self.othello.board.count("●") - self.othello.board.count("○")

    # 状態のリセット
    def reset_board_status(self):
        self.reward = 0

    #------------------------------------------
    # 盤面生成(テストプレイ用)
    def set_test_game(self):
        self.othello = Othello()
        self.othello.test_start_play()

    def test_player_play(self):
        self.othello.test_player_play()

    def test_ai_play(self, action):
        x = int(action % 8)
        y = int(action / 8)
        return self.othello.test_ai_play(x, y)

    #------------------------------------------
    # 盤面生成(学習用)
    def set_new_game(self):
        self.othello = Othello()
        self.othello.learning_start_play()

    def learning_next(self):
        self.othello.learning_next()

    # 手を選んで置く
    def learning_play(self, action):
        self.reward = 0

        x = int(action % 8)
        y = int(action / 8)
        return self.othello.learning_play(x, y)

    # 盤上を見ずにランダムに置く
    def random_play(self):
        return self.othello.learning_play(random.randint(0, 7), random.randint(0, 7))

    def is_playable(self):
        return self.othello.is_playable()

    def is_available(self):
        availables = self.othello.board.availables("●")
        # print "is_available : " + str(availables)
        if not availables:
            return False
        else:
            return True

    def print_board(self):
        print(self.othello.board)

    def show_result(self):
        self.othello.show_result(self.othello.board)
