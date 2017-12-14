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

    env.reset_board_status()
    env.set_new_game()

