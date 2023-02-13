<h3>Data analysis</h3> 
In notebook analyze_data check the distribution of the labels in the dataset as well as video format

<h3>Frame exraction</h3> 
For the first set of experiments I decided to use every 10th frame. (3fps)

Frames are exracted using ffmpeg library and python scripting

[Faster Way] use the command below and then remane frame names since ffmpeg does not allow filename formatting. 

ffmpeg -i ./images/test/test.mp4 -vf "select=not(mod(n\,10))" -vsync vfr ./frames/test/test_frame_%03d.png

python extract_frames.py ./data/images/test/test.mp4 10 ./data/frames/test test_frame

-> Fix:
ffmpeg conditioning was causing frame delay in extraction. Reverted to extracting all frames with 'ffmpeg -i <source> <target>' and then
deleting intermediate files. 


<h3>Data Formatting</h3> 

json2yolo7.py is used to convert the images to the yolo format data



