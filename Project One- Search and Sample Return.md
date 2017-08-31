# Project One: Search and Sample Return

## Section I

_Describe in your writeup (and identify where in your code) how you modified or added functions to add obstacle and rock sample identification_

Used color thresholding to identify rocks, obstance identification. See `color_thresh_rock()` and `color_thresh_obstacle()` for more information


## Section II

_Describe in your writeup how you modified the_ `process_image()` _to demonstrate your analysis and how you created a worldmap. Include your video output with your submission._

`process_image()` steps are:

- Pass an image, from the perspective of the Rover.
- The current x,y positions and yaw are obtained from `data`.
- The current image is mapped onto the area using perspective transform
- The visual information - navigable ground, obstructions and samples - is extracted by applying color thresholds.
- The masked images are mapped onto the world map by aligning the coordinates (using polor coord).
- The output is an image with the masks applied to different layers.


## Section III

`perception_step()` _and_ `decision_step()` _functions have been filled in and their functionality explained in the writeup._

### `perception_step()`
- Perspective transform of the rover's front view image.
- Uses color thresholds to identify navigable path, obstacles and GOLD.
- Updates world map after converting from pixel to world positions by rotation and translation
- Updates Rover's state of the world with latest data which will be used in decision step


### `decision_step()`
Decision step identifies if the rover has been stuck in a location for last 50 steps. If the rover is stuck, it will back off and then continue running forward. Not a great intelligence but it kind of works eventually. Other than that, it is a run in the mill rover making decisions. I didn't have time to make the pick up step work yet.




## Section IV

_By running_ `drive_rover.py` _and launching the simulator in autonomous mode, your rover does a reasonably good job at mapping the environment._

_The rover must map at least 40% of the environment with 60% fidelity (accuracy) against the ground truth. You must also find (map) the location of at least one rock sample_
