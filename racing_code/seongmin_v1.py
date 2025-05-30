import math

def reward_function(params):
    speed = params['speed']
    waypoints = params['waypoints']
    closest_idx = params['closest_waypoints'][1]
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    is_offtrack = params['is_offtrack']
    steering = abs(params['steering_angle'])
    steps = params['steps']
    progress = params['progress']

    # 트랙 이탈 시 최소 보상
    if is_offtrack:
        return 1e-3  # 트랙 밖이면 거의 0 보상

    reward = 1.0  # 기본 보상 시작

    # upcoming turn angle 계산
    if closest_idx < len(waypoints) - 1:
        next_point = waypoints[closest_idx]
        prev_point = waypoints[closest_idx - 1]
        next_next_point = waypoints[(closest_idx + 1) % len(waypoints)]

        track_direction = math.degrees(math.atan2(
            next_point[1] - prev_point[1],
            next_point[0] - prev_point[0]
        ))
        upcoming_direction = math.degrees(math.atan2(
            next_next_point[1] - next_point[1],
            next_next_point[0] - next_point[0]
        ))
        turn_angle = abs(upcoming_direction - track_direction)
        if turn_angle > 180:
            turn_angle = 360 - turn_angle
    else:
        turn_angle = 0

    # 1️⃣ outline/in-line 유지
    if turn_angle < 10:  # 직선 구간
        if distance_from_center >= 0.4 * track_width:
            reward += 1.0  # 오른쪽 아웃라인 주행 보상
    else:  # 코너 구간
        if distance_from_center <= 0.1 * track_width:
            reward += 1.0  # 왼쪽 인코스 주행 보상

    # 2️⃣ 속도 보상 (느림 패널티, 빠름 보상)
    if speed < 2.0:
        reward *= 0.8  # 너무 느리면 패널티
    elif speed > 3.8:
        reward += 1.0  # 빠름 보상

    # 3️⃣ steering penalty
    if steering > 15:
        reward *= 0.8  # 과도한 steering 패널티

    # 4️⃣ 진행률 기반 보상 (time 압박 유도)
    expected_progress = (steps / 300) * 100  # 300 스텝 기준 예상 진행률
    if progress > expected_progress:
        reward += 1.0
    else:
        reward *= 0.9  # 너무 느리면 진행률 패널티

    return float(reward)
