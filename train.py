#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import numpy as np

from catch_ball import CatchBall
from dqn_agent import DQNAgent

if __name__ == "__main__":
    # 学習に回す回数
    n_epochs = 0
    n_game = 100



    env = CatchBall()
    agent = DQNAgent(env.enable_actions, env.name)
    total_result_log = ""

    for e in range(n_game):
        # るーぷ開始地点
        frame = 0
        win = 0
        loss = 0.0
        Q_max = 0.0
        env.reset_board_status()
        env.set_new_game()
        state_after = env.observe()

        # 1ゲーム内の処理開始地点
        while env.is_playable() is True:
            # print "*********************************************************************************"

            state_before = copy.deepcopy(state_after)

            # 自分の手がOKになるまでループ（置けないところに置く可能性がある為）
            while True is True:
                env.is_available()

                # 手を選ばせる。盤面情報と手のブレ率（random)を与える
                # hand_result = env.random_play()
                action_t = agent.select_action(state_before, agent.exploration)
                hand_result = env.learning_play(action_t)

                if hand_result == "ok":
                    break
                elif hand_result == "ng":
                    state_after = env.observe_ng(action_t)
                    reward_t = -9999
                    agent.store_experience(state_before, action_t, reward_t, state_after, env.is_playable())
                    agent.experience_replay(n_epochs)
                    n_epochs+=1
                    frame += 1
                    loss += agent.current_loss
                    Q_max += np.max(agent.Q_values(state_before))
                    print "EPOCH: {:03d} | WIN: {:03d} | LOSS: {:.4f} | Q_MAX: {:.4f}".format(n_epochs, win, loss / frame, Q_max / frame)
                elif hand_result == "pass":
                    break
                else:
                    print "Hung up"

            # 相手の手を進める（基本的に相手が後攻）
            env.learning_next()

            # 1手毎の結果を処理する
            if hand_result == "pass":
                # print "pass"
                pass
            else:
                state_after = env.observe()
                reward_t = env.get_stone_reward()

                agent.store_experience(state_before, action_t, reward_t, state_after, env.is_playable())
                agent.experience_replay(n_epochs)
                n_epochs+=1
                frame += 1
                loss += agent.current_loss
                Q_max += np.max(agent.Q_values(state_before))
                if reward_t == 1:
                    win += 1
            
            print "EPOCH: {:03d} | WIN: {:03d} | LOSS: {:.4f} | Q_MAX: {:.4f}".format(n_epochs, win, loss / frame, Q_max / frame)

        # 結果を表示
        # env.print_board()
        env.show_result()

        # print("EPOCH: {:03d}/{:03d} | WIN: {:03d} | LOSS: {:.4f} | Q_MAX: {:.4f}".format(e, n_epochs - 1, win, loss / frame, Q_max / frame))
        # total_result_log += "EPOCH: {:03d}/{:03d} | WIN: {:03d} | LOSS: {:.4f} | Q_MAX: {:.4f}".format(e, n_epochs - 1, win, loss / frame, Q_max / frame) + str("\n")

    print total_result_log
    agent.save_model()
