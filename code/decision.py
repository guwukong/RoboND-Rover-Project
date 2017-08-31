import numpy as np
from time import time
import collections


# This is where you can build a decision tree for determining throttle, brake and steer
# commands based on the output of the perception_step() function
def decision_step(Rover):

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!

    # Example:
    # Check if we have vision data to make decisions with
    Rover.last_ten_positions.append(Rover.pos)
    if(len(Rover.last_ten_positions) == 50) :
        Rover.isStuck = all(abs(x[0] - Rover.last_ten_positions[0][0]) <= 0.1 and abs(x[1] - Rover.last_ten_positions[0][1]) <= 0.1 for x in Rover.last_ten_positions)

    if not Rover.time_random_check:
        Rover.time_random_check = time()
        Rover.current_position = []


    if Rover.nav_angles is not None:
        if (int(Rover.time_random_check) % 2) == 0:
            Rover.current_position.append(Rover.pos)
            if (int(Rover.time_random_check) % 5) == 0:
                Rover.curX =  [x[0] for x in Rover.current_position]
                Rover.curY = [y[1] for y in Rover.current_position]
                while (Rover.pos[0] > np.min(Rover.curX)) and (Rover.pos[0] < np.max(Rover.curX)) and (Rover.pos[1] > np.min(Rover.curY)) and (Rover.pos[1] < np.max(Rover.curX)):
                    new_time =  time()
                    while True:
                        Rover.brake = 0
                        Rover.steer = random.choice([-1,1])*15
                        if(time() - new_time) > 3.0:
                            Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -1, 1)
                            if(Rover.isStuck) :
                                Rover.throttle = -5
                            else:
                                Rover.throttle = 10
                            if (time() - new_time) > 4.0:
                                break
                Rover.current_position = []

        # Check for Rover.mode status
        if Rover.mode == 'forward':
            Rover.stopped = False
            Rover.stopped_time = None
            # Check the extent of navigable terrain
            if len(Rover.nav_angles) >= Rover.stop_forward:
                # If mode is forward, navigable terrain looks good
                # and velocity is below max, then throttle
                if (Rover.vel < Rover.max_vel) :
                    if (Rover.vel <= 0) and (Rover.started) and not Rover.isStuck:
                        Rover.throttle = 0
                        # Release the brake to allow turning
                        Rover.brake = 0
                        Rover.stopped = time()
                        while Rover.stopped < 4:
                            # Turn range is +/- 20 degrees, when stopped the next line will induce 4-wheel turning
                            Rover.steer = -20
                            Rover.stopped = None
                        Rover.throttle = 10
                        Rover.mode = 'stop'
                    else:
                        # Set throttle value to throttle setting
                        Rover.throttle = Rover.throttle_set
                        Rover.started = True
                else: # Else coast
                    Rover.throttle = 0
                Rover.brake = 0
                Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -1*np.std(Rover.nav_angles * 180/np.pi), 1*np.std(Rover.nav_angles * 180/np.pi))

                if Rover.isStuck:
                    Rover.throttle = -10
                    Rover.steer = np.random.normal(0.0, 1.0, 1)
                    Rover.steer = np.mean(Rover.nav_angles * 180/np.pi) + 6 * np.std(Rover.nav_angles * 180/np.pi)
                # Set steering to average angle clipped to the range +/- 15
            # If there's a lack of navigable terrain pixels then go to 'stop' mode
            elif len(Rover.nav_angles) < Rover.stop_forward:
                    # Set mode to "stop" and hit the brakes!
                    Rover.throttle = 0
                    # Set brake to stored brake value
                    Rover.brake = Rover.brake_set
                    Rover.steer = 0
                    Rover.mode = 'stop'

        # If we're already in "stop" mode then make different decisions
        elif Rover.mode == 'stop':
            Rover.stopped = True

            # If we're in stop mode but still moving keep braking
            if Rover.vel > 0.2:
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
            # If we're not moving (vel < 0.2) then do something else
            elif Rover.vel <= 0.2:
                # Now we're stopped and we have vision data to see if there's a path forward
                if len(Rover.nav_angles) < Rover.go_forward:
                    Rover.throttle = 0
                    # Release the brake to allow turning
                    Rover.brake = 0
                    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                    Rover.steer = -15 # Could be more clever here about which way to turn
                # If we're stopped but see sufficient navigable terrain in front then go!
                if len(Rover.nav_angles) >= Rover.go_forward:
                    # Set throttle back to stored value
                    Rover.throttle = Rover.throttle_set
                    # Release the brake
                    Rover.brake = 0
                    # Set steer to mean angle
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
                    Rover.mode = 'forward'
    # Just to make the rover do something
    # even if no modifications have been made to the code
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0

    # If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and Rover.vel == 0:
        Rover.send_pickup = True


    return Rover
