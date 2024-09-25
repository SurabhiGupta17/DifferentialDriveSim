def going_straight(robot_speed):
    v_left = robot_speed
    v_right = robot_speed
    return v_left, v_right

def turning_left(robot_speed):
    v_left = robot_speed * 0.95  # Slow down left wheel
    v_right = robot_speed         # Keep right wheel at full speed
    return v_left, v_right

def turning_right(robot_speed):
    v_left = robot_speed         # Keep left wheel at full speed
    v_right = robot_speed*0.95  # Slow down right wheel
    return v_left, v_right

def accelerating(start_speed, end_speed, duration):
    steps = 10  # Number of steps
    speed_increment = (end_speed - start_speed) / steps
    scenarios = []
    for i in range(steps + 1):
        v_left = start_speed + i * speed_increment
        v_right = start_speed + i * speed_increment
        scenarios.append((v_left, v_right))
    return scenarios

def decelerating(start_speed, end_speed, duration):
    steps = 10  # Number of steps
    speed_increment = (start_speed - end_speed) / steps
    scenarios = []
    for i in range(steps + 1):
        v_left = start_speed - i * speed_increment
        v_right = start_speed - i * speed_increment
        scenarios.append((v_left, v_right))
    return scenarios

def turning_on_the_spot(robot_speed):
    v_left = robot_speed
    v_right = -robot_speed  # Opposite speeds for turning on the spot
    return v_left, v_right
