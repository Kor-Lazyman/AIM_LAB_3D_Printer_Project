# RL-based-PD-for-AM
주요 라이브러리 :

gym: 시뮬레이션 환경, 설치법:pip install gym

sb3: gym환경 기반의 심층강화학습 라이브러리, 설치법: pip install stable-baselines3

Trimesh: 3D모델을 자르는 기능을 제공하는 라이브러리, 설치법 pip install trimesh

tensorboard: 학습의 경과를 보여주는 시각화 툴, 설치법: pip install tensorboard

config.py 강화학습에 필요한 데이터가 담겨져 있는 파일

config 파일 내 변수

N_EPISODES: 총 절삭 횟수(너무 작을시 2048회로 설정)

N_EVAL_EPISODES: 평가 반복수

MAX_N_PARTS: 부품수가 최소한 넘어야 하는 개수

TRAIN: 학습과정을 기록하는 변수

EXTENDED: tweaker가 더 정확하게 회전을 하게 만들어 주는 변수

INPUT_MODEL: 강화 학습으로 최적화 할 3D 모델명

IMPORT_DIR: 가져올 폴더



학습 실행법: cmd를 통해 설치된 폴더의 경로의 src폴더에 들어가 python main.py를 입력

결과 시각화 실행법: tensorboard --logdir="설치된 폴더의 경로/src/logs"
		EX)tensorboard --logdir=C:\Users\User\Downloads\AIM_LAB_3D_Printer_Project-main\AIM_LAB_3D_Printer_Project-main\RL_based_PD_for_AM-main\RL_based_PD_for_AM-main\src\logs
