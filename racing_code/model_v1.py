import math

def reward_function(params):
    speed = params['speed']
    steering = abs(params['steering_angle'])
    heading = params['heading']
    waypoints = params['waypoints']
    closest_idx = params['closest_waypoints']
    progress = params['progress']
    steps = params['steps']
    is_offtrack = params['is_offtrack']
    is_crashed = params['is_crashed']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    all_wheels_on_track = params['all_wheels_on_track']

    if is_offtrack or is_crashed:
        return 0.001

    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    if distance_from_center <= marker_1:
        center_reward = 1.0
    elif distance_from_center <= marker_2:
        center_reward = 0.5
    else:
        center_reward = 0.001

    next_point = waypoints[closest_idx[1]]
    prev_point = waypoints[closest_idx[0]]
    track_direction = math.degrees(math.atan2(
        next_point[1] - prev_point[1],
        next_point[0] - prev_point[0]
    ))
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff
    direction_reward = max(1.0 - (direction_diff / 50), 0.0)

    speed_threshold = 3.5
    if direction_diff < 10:
        speed_reward = min(speed / speed_threshold, 1.0)
    else:
        speed_reward = 1.0 if speed < speed_threshold else 0.5

    steering_penalty = 1.0 if steering < 15 else 0.8

    expected_progress = (steps / 300) * 100
    progress_reward = 1.0 if progress > expected_progress else 0.5

    reward = (
        2.0 * center_reward +
        2.0 * speed_reward +
        1.5 * direction_reward +
        1.0 * steering_penalty +
        1.0 * progress_reward
    )

    return float(max(reward, 0.001))
    