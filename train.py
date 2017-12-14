#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import numpy as np

from catch_ball import CatchBall
from dqn_agent import DQNAgent


if __name__ == "__main__":
    # 学習に回す回数
    n_epochs = 10000

    env = CatchBall()
    # agent = DQNAgent(env.enable_actions, env.name)


# るーぷ開始地点
    env.reset_board_status()
    env.set_new_game()


# 1ゲーム内の処理開始地点

    is_abort = False

    while env.is_playable() is True and is_abort is False:
        env.learning_next()
        hand_result = ""
        while hand_result != "ok" and is_abort is False:
            hand_result = env.learning_play()
            if hand_result == "pass":
                print "end"
                is_abort = True

