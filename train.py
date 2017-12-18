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
    agent = DQNAgent(env.enable_actions, env.name)

    # for e in range(n_epochs):
    # るーぷ開始地点
    is_abort = False
    frame = 0
    loss = 0.0
    Q_max = 0.0
    env.reset_board_status()
    env.set_new_game()
    state_t_1 = env.observe()

    # 1ゲーム内の処理開始地点
    while env.is_playable() is True and is_abort is False:
        print "*********************************************************************************"

        state_t = copy.deepcopy(state_t_1)

        # 自分の手がOKになるまでループ（置けないところに置く可能性がある為）
        while is_abort is False:
            # 手を選ばせる。盤面情報と手のブレ率（random)を与える
            # hand_result = env.random_play()
            action_t = agent.select_action(state_t, agent.exploration)
            hand_result = env.learning_play(action_t)

            if hand_result == "ok":
                break

        # 相手の手を進める（基本的に相手が後攻）
        env.learning_next()

        state_t_1 = env.observe()

        env.print_board()
        print "Result " + str(env.get_stone_reward())
