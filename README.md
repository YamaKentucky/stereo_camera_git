# stereo_camera_git
This Python script is for detecting the position coordinates of a marker using a stereo camera.

## Requirement
Soft:OpenCV2 Hard:stereo camera, infrared LED marker

## usage
- Create a "calibration" folder in the working directory.
And save the photos of the same chess board taken with the left and right stereo cameras under the name "left0" ~ "left20". Here, the number of left and right shots is not particularly determined. The accuracy of calibration will be better if there are around 20 sheets. 
However, the first photo should start with "left0" and "right0".

- Run "calibrate" in the same directory in Python. 
This will create multiple CSV files in which parameters such as camera matrix are saved. These will be used in later calculations.

- Create "left_movie" on the working directory, and put the video shot with the left camera of the video you want to detect. 
At this time, the video should be in the "* .avi" format. Where * is a number starting from 0. Execute "combine_1.py" in "left_movie" to combine multiple videos into one video. Similarly, the video shot with the right camera is also combined on "right_movie". 
When this is executed, "combined_movie.avi" is created.

- If you run "avi_to_png_kai_0.py", you will get a video converted to PNG in the directory "png_file" based on the video of "combined_movie.avi".
