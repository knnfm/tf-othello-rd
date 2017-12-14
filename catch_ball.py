#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ゲームと評価を繋ぐところ

import os
import random
import numpy as np

from othello import Othello

class CatchBall:
    def __init__(self):
        self.name = os.path.splitext(os.path.basename(__file__))[0]

    # 盤面生成
    def set_new_game(self):
        self.othello = Othello()
        self.othello.learning_start_play()

    # 状態のリセット
    def reset_board_status(self):
        self.reward = 0
        self.terminal = False

    def learning_next(self):
        self.othello.learning_next()

    def learning_play(self):
        return self.othello.learning_play(random.randint(0, 7), random.randint(0, 7))

    def is_playable(self):
        return self.othello.is_playable()