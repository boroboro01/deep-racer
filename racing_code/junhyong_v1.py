def reward_function(params):
    '''
    Example of rewarding the agent to follow center line
    '''
    reward = 1e-3

    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    steering = params['steering_angle']
    speed = params['speed']
    all_wheels_on_track = params['all_wheels_on_track']

    # reward for staying near the center
    if distance_from_center >= 0.0 and distance_from_center <= 0.03:
        reward = 1.0

    # penalty or reward based on whether wheels are on track
    if not all_wheels_on_track:
        reward = reward - 1
    else:
        reward = reward + (params['progress'])

    # add speed penalty or bonus
    if speed < 2.68:
        reward *= 0.80
    elif speed >= 2.68 and speed <= 5.33:
        reward += speed
    else:
        reward = speed * speed + reward

    return float(reward)
