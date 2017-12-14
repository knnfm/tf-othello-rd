#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ゲームと評価を繋ぐところ

import os
import numpy as np

from othello import Othello

class CatchBall:
    def __init__(self):
        self.name = os.path.splitext(os.path.basename(__file__))[0]

    # 盤面生成
    def set_new_game(self):
        self.othello = Othello()
        self.othello.play()

    # 状態のリセット
    def reset_board_status(self):
        self.reward = 0
        self.terminal = False
