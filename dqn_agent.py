#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 評価の定義をするところ

from collections import deque
import os

import numpy as np
import tensorflow as tf


class DQNAgent:
    """
    Multi Layer Perceptron with Experience Replay
    """

    def __init__(self, enable_actions, environment_name):
        # parameters
        self.board_side_size = 8
        self.board_max_size = self.board_side_size ** 2
        self.name = os.path.splitext(os.path.basename(__file__))[0]
        self.environment_name = environment_name
        self.enable_actions = enable_actions
        self.n_actions = len(self.enable_actions)
        self.minibatch_size = 32
        self.replay_memory_size = 1000
        self.learning_rate = 0.001
        self.discount_factor = 0.9
        self.exploration = 0.1
        self.model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
        self.model_name = "{}.ckpt".format(self.environment_name)
        self.D = deque(maxlen=self.replay_memory_size)
        self.win = 0
        self.win_t = tf.placeholder(tf.float32)
        self.current_loss = 0
        self.current_loss_t = tf.placeholder(tf.float32)
        self.init_model()

    def init_model(self):
        log_dir = './logs'
        if tf.gfile.Exists(log_dir):
            tf.gfile.DeleteRecursively(log_dir)
        tf.gfile.MakeDirs(log_dir)

        # input layer
        self.x = tf.placeholder(tf.float32, [None, self.board_side_size, self.board_side_size])

        # flatten
        x_flat = tf.reshape(self.x, [-1, self.board_max_size])

        # fully connected layer (32)
        W_fc1 = tf.Variable(tf.truncated_normal([self.board_max_size, self.board_max_size], stddev=0.01))
        b_fc1 = tf.Variable(tf.zeros([self.board_max_size]))
        h_fc1 = tf.nn.relu(tf.matmul(x_flat, W_fc1) + b_fc1)

        # output layer (n_actions)
        W_out = tf.Variable(tf.truncated_normal([self.board_max_size, self.n_actions], stddev=0.01))
        b_out = tf.Variable(tf.zeros([self.n_actions]))
        self.y = tf.matmul(h_fc1, W_out) + b_out

        # loss function
        self.y_ = tf.placeholder(tf.float32, [None, self.n_actions])
        self.loss = tf.reduce_mean(tf.square(self.y_ - self.y))

        # train operation
        # optimizer = tf.train.RMSPropOptimizer(self.learning_rate)
        optimizer = tf.train.AdamOptimizer(self.learning_rate)
        self.training = optimizer.minimize(self.loss)

        # saver
        self.saver = tf.train.Saver()

        # session
        self.sess = tf.Session()

        # TensorBoard
        tf.summary.scalar("win", self.win_t)
        tf.summary.scalar("loss", self.current_loss_t)
        self.summary_merged = tf.summary.merge_all()
        self.summary_writer = tf.summary.FileWriter(log_dir, self.sess.graph)

        self.sess.run(tf.global_variables_initializer())

    def Q_values(self, state):
        # Q(state, action) of all actions
        # print state

        return self.sess.run(self.y, feed_dict={self.x: [state]})[0]

    def select_action(self, state, epsilon):
        if np.random.rand() <= epsilon:
            return np.random.choice(self.enable_actions)
        else:
            return self.enable_actions[np.argmax(self.Q_values(state))]

    def store_experience(self, state, action, reward, state_1, terminal):
        self.D.append((state, action, reward, state_1, terminal))

    def experience_replay(self, count):
        state_minibatch = []
        y_minibatch = []

        # sample random minibatch
        minibatch_size = min(len(self.D), self.minibatch_size)
        minibatch_indexes = np.random.randint(0, len(self.D), minibatch_size)

        for j in minibatch_indexes:
            state_j, action_j, reward_j, state_j_1, terminal = self.D[j]
            action_j_index = self.enable_actions.index(action_j)

            # print state_j
            # print state_j_1
            y_j = self.Q_values(state_j)

            if terminal:
                # print state_j
                y_j[action_j_index] = reward_j
            else:
                y_j[action_j_index] = reward_j + self.discount_factor * np.max(self.Q_values(state_j_1))  # NOQA

            state_minibatch.append(state_j)
            y_minibatch.append(y_j)

        self.sess.run(self.training, feed_dict={self.x: state_minibatch, self.y_: y_minibatch})
        # if terminal:
        # print state_minibatch[len(state_minibatch)-1]
        # print y_minibatch[len(y_minibatch)-1]
        # print "-----------------------------"

        self.current_loss = self.sess.run(self.loss, feed_dict={self.x: state_minibatch, self.y_: y_minibatch})

        # TensorBoard
        summary = self.sess.run(self.summary_merged, feed_dict={self.current_loss_t: self.current_loss, self.win_t: self.win})
        self.summary_writer.add_summary(summary, count)
        self.summary_writer.flush()

    def load_model(self, model_path=None):
        if model_path:
            # load from model_path
            self.saver.restore(self.sess, model_path)
        else:
            # load from checkpoint
            checkpoint = tf.train.get_checkpoint_state(self.model_dir)
            if checkpoint and checkpoint.model_checkpoint_path:
                self.saver.restore(self.sess, checkpoint.model_checkpoint_path)

    def save_model(self):
        self.saver.save(self.sess, os.path.join(self.model_dir, self.model_name))
