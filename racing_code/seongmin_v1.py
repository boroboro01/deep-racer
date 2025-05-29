import math

def reward_function(params):
    speed = params['speed']
    waypoints = params['waypoints']
    closest_idx = params['closest_waypoints'][1]
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    is_offtrack = params['is_offtrack']
    steering = abs(params['steering_angle'])

    if is_offtrack:
        return 1e-3

    reward = 1.0

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
    if turn_angle < 10:
        if distance_from_center >= 0.4 * track_width:
            reward += 1.0  # 직선: 오른쪽
    else:
        if distance_from_center <= 0.1 * track_width:
            reward += 1.0  # 코너: 왼쪽

    # 2️⃣ 속도 보상 (느림 패널티, 빠름 보상)
    if speed < 2.5:
        reward *= 0.8  # 너무 느리면 패널티
    elif speed > 3.8:
        reward += 1.0  # 빠름 보상

    # 3️⃣ (선택) steering penalty
    if steering > 15:
        reward *= 0.8  # 과도한 steering 패널티

    return float(reward)