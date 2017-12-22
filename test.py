#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

import argparse
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from catch_ball import CatchBall
from dqn_agent import DQNAgent
from debug_log import DebugLog

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model_path")
    args = parser.parse_args()

    env = CatchBall()
    agent = DQNAgent(env.enable_actions, env.name)
    agent.load_model(args.model_path)

    env.reset_board_status()
    env.set_test_game()

    # 1ゲーム内の処理開始地点
    while env.is_playable() is True:
        env.print_board()
        env.test_player_play()

        state = env.observe()

        
        while True is True:
            action = agent.select_action(state, 0.0)
            hand_result = env.test_ai_play(action)
            if hand_result == "ok":
                break
            elif hand_result == "ng":
                pass
            elif hand_result == "pass":
                break
            else:
                print "Hung up"
