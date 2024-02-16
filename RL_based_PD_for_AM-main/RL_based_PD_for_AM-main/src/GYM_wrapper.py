import gym
from gym import spaces
import numpy as np
from config import *
import PD_environment as env
import os


class GymInterface(gym.Env):
    def __init__(self):
        super(GymInterface, self).__init__()
        # Define action space
        # Initialize the array for 6 actions (3 for center coordination, 3 for cutting plane angle)
        actionSize = 7
        # Create arrays for low and high values.
        # Use np.concatenate to combine the ranges for the two parts.
        '''
        low = np.concatenate(
            (np.full(3, ACTION_SPACE_CENTER_COOR_LOW), np.full(3, ACTION_SPACE_CUT_PLANE_ANGLE_LOW)))
        high = np.concatenate(
            (np.full(3, ACTION_SPACE_CENTER_COOR_HIGH), np.full(3, ACTION_SPACE_CUT_PLANE_ANGLE_HIGH)))
        # Define the action space as a Box object.
        '''

      

        # Define observation space:
        # os = [INVEN_LEVEL_MAX+1 for _ in range(len(I))]
      

        # Initialize the PD environment
        self.PD_tree, self.decomposed_parts = env.create_env()

        self.observation_space = spaces.Box(low=0, high=len(self.decomposed_parts), dtype=int)

        self.x=self.PD_tree[1]["Mesh"].vertices[:,0]
        self.y=self.PD_tree[1]["Mesh"].vertices[:,1]
        self.z=self.PD_tree[1]["Mesh"].vertices[:,2]
        self.define_action_space()
        self.total_reward_over_episode = []
        self.total_reward = 0
        self.num_episode = 1

    def define_action_space(self):
        self.action_space_low = np.concatenate([
            [0],
            [np.min(self.x, axis=0)],
            [np.min( self.y, axis=0)],
            [np.min( self.z, axis=0)],
            [np.min( self.x, axis=0)],
            [np.min( self.y, axis=0)],
            [np.min( self.z, axis=0)],
        ])
        self.action_space_high = np.concatenate([
            [len(self.decomposed_parts)-1],
            [np.max( self.x, axis=0)],
            [np.max( self.y, axis=0)],
            [np.max( self.z, axis=0)],
            [np.max( self.x, axis=0)],
            [np.max( self.y, axis=0)],
            [np.max( self.z, axis=0)],
        ])
        self.action_space = spaces.Box(low=self.action_space_low, high=self.action_space_high, dtype=np.float32)

    def reset(self):
        # Initialize the PD environment
        print("\nEpisode: ", self.num_episode)
        self.PD_tree, self.decomposed_parts = env.create_env()
        self.define_action_space()
        return self.decomposed_parts 

    def step(self, action):
        done=False
        # Update the action of the agent
        self.PD_tree, self.decomposed_parts,reward = env.decompose_parts(
            action, self.decomposed_parts,self.PD_tree)
        # Capture the next state of the environment
        self.observation_space = spaces.Box(low=0, high=len(self.decomposed_parts), dtype=int)
        # Calculate the reward
        self.define_action_space()
        self.total_reward += reward
        # 한 에피소드 종료 조건
        if MAX_N_PARTS < len(self.decomposed_parts):
            done = True
        if done == True:
            print("Total reward: ", self.total_reward)
            self.total_reward_over_episode.append(self.total_reward)
            self.total_reward = 0
            self.num_episode += 1

        info = {}  # 추가 정보 (필요에 따라 사용)
        
        return self.observation_space.sample(), reward, done, info

    def render(self, mode='human'):
        pass
        # if EPISODES == 1:
        #     self.visualize()
        # else:
        #     if OPTIMIZE_HYPERPARAMETERS:
        #         pass
        #     else:
        #         self.visualize()

    def close(self):
        # 필요한 경우, 여기서 리소스를 정리
        pass
