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
        self.enable_actions = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64)

    # 現在の盤面を取得
    def observe(self):
        board = np.array([])

        for a in self.othello.get_board_square():
            if a is "●":  # 黒
                board = np.append(board, 1)
            elif a is "○":  # 白
                board = np.append(board, -1)
            else:
                board = np.append(board, 0)

        return np.array(board, dtype=np.int32)

    # 評価を取得
    def get_reward(self):
        return 0

    # 盤面生成
    def set_new_game(self):
        self.othello = Othello()
        self.othello.learning_start_play()

    # 状態のリセット
    def reset_board_status(self):
        self.reward = 0

    def learning_next(self):
        self.othello.learning_next()

    # 手を選んで置く
    def learning_play(self, action):
        self.reward = 0

        x = action % 7
        y = action / 7
        return self.othello.learning_play(x, y)

    # 盤上を見ずにランダムに置く
    def random_play(self):
        return self.othello.learning_play(random.randint(0, 7), random.randint(0, 7))

    def is_playable(self):
        return self.othello.is_playable()
