import gym
from gym import spaces
import numpy as np
from config import *
import PD_environment as env


class GymInterface(gym.Env):
    def __init__(self):
        super(GymInterface, self).__init__()
        # Define action space
        # Initialize the array for 6 actions (3 for center coordination, 3 for cutting plane angle)
        actionSize = 6
        # Create arrays for low and high values.
        # Use np.concatenate to combine the ranges for the two parts.
        low = np.concatenate(
            (np.full(3, ACTION_SPACE_CENTER_COOR_LOW), np.full(3, ACTION_SPACE_CUT_PLANE_ANGLE_LOW)))
        high = np.concatenate(
            (np.full(3, ACTION_SPACE_CENTER_COOR_HIGH), np.full(3, ACTION_SPACE_CUT_PLANE_ANGLE_HIGH)))
        # Define the action space as a Box object.
        action_space = spaces.Box(low=low, high=high, dtype=np.float32)

        # Define observation space:
        # os = [INVEN_LEVEL_MAX+1 for _ in range(len(I))]
        # if STATE_DEMAND:
        #     os.append(DEMAND_QTY_MAX - DEMAND_QTY_MIN + 1)
        self.observation_space = spaces.MultiDiscrete(os)

        # Initialize the PD environment
        self.PD_tree, self.decomposed_parts = env.create_env()
        self.total_reward_over_episode = []
        self.total_reward = 0
        self.num_episode = 1

    def reset(self):
        # Initialize the PD environment
        print("\nEpisode: ", self.num_episode)
        self.PD_tree, self.decomposed_parts = env.create_env()
        return env.cap_current_state(self.PD_tree, self.decomposed_parts)

    def step(self, action):
        # Update the action of the agent
        self.PD_tree, self.decomposed_parts = env.decompose_parts(
            action)
        # Capture the next state of the environment
        next_state = env.cap_current_state(
            self.PD_tree, self.decomposed_parts)
        # Calculate the reward
        reward = env.cal_reward(next_state)
        self.total_reward += reward
        # 한 에피소드 종료 조건
        if MAX_N_PARTS == len(self.decomposed_parts):
            done = True
        if done == True:
            print("Total reward: ", self.total_reward)
            self.total_reward_over_episode.append(self.total_reward)
            self.total_reward = 0
            self.num_episode += 1

        info = {}  # 추가 정보 (필요에 따라 사용)
        return next_state, reward, done, info

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
