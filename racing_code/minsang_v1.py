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

    # 트랙 방향 계산
    next_point = waypoints[closest_idx]
    prev_point = waypoints[closest_idx - 1]
    track_direction = math.degrees(math.atan2(
        next_point[1] - prev_point[1],
        next_point[0] - prev_point[0]
    ))
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # 코너 여부 판별
    if closest_idx < len(waypoints) - 1:
        next_next_point = waypoints[(closest_idx + 1) % len(waypoints)]
        upcoming_direction = math.degrees(math.atan2(
            next_next_point[1] - next_point[1],
            next_next_point[0] - next_point[0]
        ))
        turn_angle = abs(upcoming_direction - track_direction)
        if turn_angle > 180:
            turn_angle = 360 - turn_angle
    else:
        turn_angle = 0

    # 기본 보상
    reward = 1.0

    # 최적 주행선: 트랙 중심보다 살짝 바깥쪽 (0.2 * track_width)
    optimal_marker = 0.2 * track_width
    if distance_from_center <= optimal_marker:
        reward += 1.0
    else:
        reward *= 0.7

    # 코너 구간: steering 높을수록 감속, 탈출 시 재가속
    if turn_angle > 15:
        if steering > 15 and speed < 2.0:
            reward += 2.0  # 코너링 안정성
        elif steering < 10 and speed >= 2.0:
            reward += 2.0  # 코너 탈출 가속
    else:
        if speed >= 3.0:
            reward += 2.0  # 직선에서 속도 최적화

    # 부드러운 steering
    if steering < 10:
        reward += 1.0
    else:
        reward *= 0.8

    # 주행 방향 일치
    if direction_diff < 10:
        reward += 1.0
    else:
        reward *= 0.6

    # 오프트랙 패널티
    if is_offtrack:
        reward = 1e-3

    return float(reward)
