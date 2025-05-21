import gym
import matplotlib.pyplot as plt

# 환경 초기화
env = gym.make('CartPole-v0')

# 누적 보상을 저장할 리스트
rewards = []

for episode in range(100):  # 100 에피소드 진행
    state = env.reset()
    done = False
    total_reward = 0
    while not done:
        env.render()  # 환경을 화면에 표시

        # 무작위로 행동 선택
        action = env.action_space.sample()

        # 선택한 행동을 환경에 적용
        next_state, reward, done, _ = env.step(action)
        total_reward += reward

        # 선택한 액션, 보상, 환경 상태, 누적 리워드 출력
        print(f"Action: {action}, Reward: {reward}, State: {next_state}, Total Reward: {total_reward}")

        state = next_state

    rewards.append(total_reward)

env.close()

# 누적 보상 시각화
plt.plot(rewards)
plt.xlabel('Episode')
plt.ylabel('Total Reward')
plt.title('Total Reward over Episodes')
plt.show()
