import math

def reward_function(params):
    speed = params['speed']
    steering = abs(params['steering_angle'])
    heading = params['heading']
    waypoints = params['waypoints']
    closest_idx = params['closest_waypoints'][1]
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    is_offtrack = params['is_offtrack']
    progress = params['progress']
    steps = params['steps']

    # 학습 진행률 (adaptive weight용)
    training_fraction = steps / 100000  # 10만 스텝 가정
    if training_fraction > 1.0:
        training_fraction = 1.0

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

    # adaptive weights (코너 → 초반 강화, 직선 → 후반 강화)
    corner_weight = 2.0 * (1 - training_fraction) + 1.0 * training_fraction
    speed_weight = 1.0 * (1 - training_fraction) + 2.0 * training_fraction

    reward = 1.0

    # optimal racing line (중앙보다 약간 바깥)
    optimal_marker = 0.2 * track_width
    if distance_from_center <= optimal_marker:
        reward += 1.0
    else:
        reward *= 0.5

    # 직선 구간 → 최대 가속
    if turn_angle < 10:
        if speed > 3.5:
            reward += speed_weight * 2.0
        if steering < 5:
            reward += 1.0
    # 코너 구간 → 감속 + 안정성
    else:
        if steering > 15 and speed < 2.0:
            reward += corner_weight * 2.0
        elif steering < 10 and speed >= 2.0:
            reward += corner_weight * 1.0  # exit boost
        else:
            reward *= 0.8

    # progress/time 압박
    expected_progress = (steps / 300) * 100  # 300 steps 기준
    if progress > expected_progress:
        reward += 1.0
    else:
        reward *= 0.9

    # 방향 정렬 보상
    next_point = waypoints[closest_idx]
    prev_point = waypoints[closest_idx - 1]
    track_direction = math.degrees(math.atan2(
        next_point[1] - prev_point[1],
        next_point[0] - prev_point[0]
    ))
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    if direction_diff < 10:
        reward += 1.0
    else:
        reward *= 0.6

    # 오프트랙 극단 패널티 (+5초 패널티 대응)
    if is_offtrack:
        reward = 1e-3

    return float(reward)
