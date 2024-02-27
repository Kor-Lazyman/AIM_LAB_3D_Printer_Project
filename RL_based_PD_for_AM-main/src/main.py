from GYM_wrapper2 import GymInterface
from config import *
import numpy as np
import time
from stable_baselines3 import PPO  # DDPG
from torch.utils.tensorboard import SummaryWriter
from stable_baselines3.common.callbacks import EvalCallback
from datetime import datetime
import matplotlib.pyplot as plt
import interface
from MeshTweaker import Tweak

# 학습 로그 및 모델 저장 디렉토리
log_dir = "./logs"


env = GymInterface()
# EvalCallback 설정


# Create environment


# Define a function to evaluate a trained model


def evaluate_model(model, env, num_episodes):
    env = GymInterface()
    all_rewards = []
    for _ in range(num_episodes):
        obs = env.reset()
        episode_reward = 0
        done=False
        while not done:
            action, _ = model.predict(obs)
            obs, reward, done, _ = env.step(action)
            episode_reward += reward

        all_rewards.append(episode_reward)
    mean_reward = np.mean(all_rewards)
    std_reward = np.std(all_rewards)

    for x in range(len(env.decomposed_parts)):
        mesh=env.PD_tree[env.decomposed_parts[x]]["Mesh"]
        mesh.export(f'./Resulted_Stl/{env.decomposed_parts[x]}.stl')
    return mean_reward, std_reward



# Train the agent
start_time = time.time()
model = PPO("MlpPolicy", env, verbose=0,device='cuda')
TRAIN=True
model.learn(total_timesteps=N_EPISODES)  # Time steps = episodes in our case
model.save("./Saved_RL_Models/PPO")
env.render()  # Render the environment to see how well it performs
cont=0



    
# Evaluate the trained agent
TRAIN=False
mean_reward, std_reward = evaluate_model(model, env, N_EVAL_EPISODES)
print(
    f"Mean reward over {N_EVAL_EPISODES} episodes: {mean_reward:.2f} +/- {std_reward:.2f}")

end_time = time.time()
print(f"Computation time: {(end_time - start_time)/3600:.2f} hours")
"""
plt.plot(env.total_reward_over_episode)
plt.show()
"""
# TensorBoard 실행:
# tensorboard --logdir="C:/tensorboard_logs/"
# http://localhost:6006/
