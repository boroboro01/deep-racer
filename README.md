# Deep Racer Reinforcement Learning Project

## 1. 프로젝트 개요
OpenAI Gym 기반 강화학습 실습 프로젝트로,  
`CartPole-v0` 무작위 행동 시뮬레이션과 `FrozenLake-v1` Q-러닝 알고리즘 예제를 포함합니다.

## 2. 주요 파일 및 결과

### `random_cartpole.py`
- CartPole 환경에서 100 에피소드 동안 무작위 행동을 수행  
- 매 에피소드별 누적 보상을 기록하고 시각화  

<img src="https://github.com/user-attachments/assets/69c8e551-d233-4a7d-a4c2-4acd9e6e15ee" width="53%" alt="CartPole 시뮬레이션 화면" />
<img src="https://github.com/user-attachments/assets/10507bff-f33b-4fee-bb8f-c6184499bb7f" width="46%" alt="누적 보상 그래프" />

- 좌측 사진: CartPole 환경에서 에이전트가 무작위 행동을 수행하는 시뮬레이션 화면  
- 우측 사진: 100 에피소드 동안 누적 보상의 변화를 나타낸 그래프  

---

### `q_learning_frozenlake.py`
- FrozenLake 환경에서 Q-러닝 알고리즘으로 학습 진행  
- 학습 과정 중 보상의 이동 평균을 그래프로 시각화  

<img src="https://github.com/user-attachments/assets/357fc920-eff9-450e-b057-ad12221e1b52" width="60%" alt="FrozenLake 보상 그래프" />

- 학습 진행에 따른 보상 이동 평균 그래프로 에이전트의 성능 향상 확인
