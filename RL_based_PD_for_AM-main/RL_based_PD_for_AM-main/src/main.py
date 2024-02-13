from GYM_wrapper import GymInterface
from config import *
import numpy as np
import time
from stable_baselines3 import PPO  # DDPG

# Create environment
env = GymInterface()

# Define a function to evaluate a trained model


def evaluate_model(model, env, num_episodes):
    all_rewards = []
    for _ in range(num_episodes):
        obs = env.reset()
        episode_reward = 0
        done = False
        while not done:
            action, _ = model.predict(obs)
            obs, reward, done, _ = env.step(action)
            episode_reward += reward
        all_rewards.append(episode_reward)
    mean_reward = np.mean(all_rewards)
    std_reward = np.std(all_rewards)
    return mean_reward, std_reward


# Train the agent
start_time = time.time()
model = PPO("MlpPolicy", env, verbose=0)
model.learn(total_timesteps=N_EPISODES)  # Time steps = episodes in our case
env.render()  # Render the environment to see how well it performs

# Evaluate the trained agent
mean_reward, std_reward = evaluate_model(model, env, N_EVAL_EPISODES)
print(
    f"Mean reward over {N_EVAL_EPISODES} episodes: {mean_reward:.2f} +/- {std_reward:.2f}")

end_time = time.time()
print(f"Computation time: {(end_time - start_time)/3600:.2f} hours")


# TensorBoard 실행:
# tensorboard --logdir="C:/tensorboard_logs/"
# http://localhost:6006/
