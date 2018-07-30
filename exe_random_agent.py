#!/usr/bin/python

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from random import random;

from gtpinterface import GTPInterface
import os
import sys
import argparse

import numpy as np
from numpy.random.mtrand import randint

#test

class RandomAgent(object):
    def __init__(self, boardsize, name):
        self.boardsize=boardsize
        self.name = name
        self.black_int_moves=[]
        self.white_int_moves=[]

    def reinitialize(self):
        pass

    '''raw_player either is 'black' or 'white'
       raw_move is something like a5, b7
    '''
    def play_move(self,raw_player, raw_move):
	int_move=(ord(raw_move[0])-ord('a'))*self.boardsize + int(raw_move[1:])-1
	if raw_player[0] == 'b':
           self.black_int_moves.append(int_move)
	else:
           self.white_int_moves.append(int_move)

    '''player is either 'black' or 'white' '''
    def generate_move(self, player):
        #return
        int_move = randint(0, self.boardsize);
        print(int_move);
        if player[0] == 'b':
            self.black_int_moves.append(int_move);
        else:
            self.white_int_moves.append(int_move);
    
    def set_boardsize(self, boardsize):
        self.boardsize=boardsize
        self.black_int_moves=[]
        self.white_int_moves=[]

def main(boardsize):
    """
    Executable of the neural net player..
    use the latest model saved by policy gradient reinforcement learning
    """

    agent=RandomAgent(boardsize, name="random_player")
    interface=GTPInterface(agent)
    while True:
        command=raw_input()
        success, response =interface.send_command(command)
        print("= " if success else "? ", response, "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description='test')
    parser.add_argument('--boardsize', type=int, default=9, help="boardsize?")
    parser.add_argument('--verbose', action='store_true', help='verbose?')
    args=parser.parse_args()
    main(args.boardsize)
