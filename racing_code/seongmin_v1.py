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

    # 직선 구간
    if turn_angle < 10:
        if distance_from_center >= 0.4 * track_width:
            reward += 1.0  # 오른쪽 아웃라인 주행 보상

        # 속도 보상 개선
        if speed < 2.0:
            reward *= 0.8  # 너무 느리면 패널티
        elif speed <= 4.0:
            reward += speed * 0.5  # 중간 속도 선형 보상
        else:
            reward += 2.0  # capped 보너스, 폭발 방지

    # 코너 구간
    else:
        if distance_from_center <= 0.1 * track_width:
            reward += 1.0  # 왼쪽 인코스 주행 보상

        # 코너 속도 보상 개선
        if speed < 2.0:
            reward += 1.0  # 저속 안전 주행 보상
        elif speed <= 3.0:
            reward += 0.5  # 약간 빠른 속도는 소폭 보상
        else:
            reward *= 0.7  # 코너에서 너무 빠르면 패널티

    # 스티어링 각도 패널티
    if steering > 15:
        reward *= 0.8

    # 진행률 기반 보상
    expected_progress = (steps / 300) * 100
    if progress > expected_progress:
        reward += 1.0
    else:
        reward *= 0.9

    return float(reward)