from GYM_wrapper import GymInterface
from config import *
import numpy as np
import time
from stable_baselines3 import PPO  # DDPG
from torch.utils.tensorboard import SummaryWriter
from stable_baselines3.common.callbacks import EvalCallback
from datetime import datetime
import matplotlib.pyplot as plt

# 학습 로그 및 모델 저장 디렉토리
log_dir = "C:/Users/taekw/Downloads/AIM_LAB_3D_Printer_Project-main/AIM_LAB_3D_Printer_Project-main/RL_based_PD_for_AM-main/RL_based_PD_for_AM-main/src/logs"
model_save_path = "models/"


env = GymInterface()
# EvalCallback 설정
eval_callback = EvalCallback(env,
                             callback_on_new_best=None,
                             n_eval_episodes=N_EVAL_EPISODES,
                             eval_freq=10000,  # 학습 단계마다 평가
                             log_path=log_dir,
                             best_model_save_path=model_save_path,
                             verbose=1)

# Create environment


# Define a function to evaluate a trained model


def evaluate_model(model, env, num_episodes):
    env = GymInterface()
    all_rewards = []
    for _ in range(num_episodes):
        obs = env.reset()
        
        episode_reward = 0
        done = False
        while not done:
            action, _ = model.predict(obs.reshape(1,))
            obs, reward, done, _ = env.step(action)
            episode_reward += reward
            print("===========")
            print(obs)
            print(done)
            print(env.decomposed_parts)
            print("===========")
            if len(env.decomposed_parts)>MAX_N_PARTS:
                done=True
        all_rewards.append(episode_reward)
    mean_reward = np.mean(all_rewards)
    std_reward = np.std(all_rewards)
    return mean_reward, std_reward


# Train the agent
start_time = time.time()
model = PPO("MlpPolicy", env, verbose=0,device='cuda', tensorboard_log=log_dir)
model.learn(total_timesteps=N_EPISODES)  # Time steps = episodes in our case
model.save("C:/Users/taekw/Downloads/AIM_LAB_3D_Printer_Project-main/AIM_LAB_3D_Printer_Project-main/RL_based_PD_for_AM-main/RL_based_PD_for_AM-main/src/Result_model/Saved_Model")
env.render()  # Render the environment to see how well it performs
cont=0

# Evaluate the trained agent
mean_reward, std_reward = evaluate_model(model, env, N_EVAL_EPISODES)
print(
    f"Mean reward over {N_EVAL_EPISODES} episodes: {mean_reward:.2f} +/- {std_reward:.2f}")

end_time = time.time()
print(f"Computation time: {(end_time - start_time)/3600:.2f} hours")

plt.plot(env.total_reward_over_episode)
plt.show()
# TensorBoard 실행:
# tensorboard --logdir="C:/tensorboard_logs/"
# http://localhost:6006/
