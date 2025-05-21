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
        env.render()  # 환경 화면 출력
        
        # 무작위 행동 선택
        action = env.action_space.sample()
        
        # 행동 적용 및 결과 수신
        next_state, reward, done, _ = env.step(action)
        total_reward += reward
        
        # 행동과 보상 출력
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
