def going_straight(robot_speed):
    v_left = robot_speed
    v_right = robot_speed
    return v_left, v_right

def turning_left(robot_speed):
    v_left = robot_speed * 0.95  
    v_right = robot_speed         
    return v_left, v_right

def turning_right(robot_speed):
    v_left = robot_speed        
    v_right = robot_speed * 0.95  
    return v_left, v_right

def accelerating(robot_speed):
    return robot_speed + 5

def decelerating(robot_speed):
    return max(0, robot_speed - 5)

def turning_on_the_spot(robot_speed):
    v_left = robot_speed
    v_right = -robot_speed 
    return v_left, v_right
