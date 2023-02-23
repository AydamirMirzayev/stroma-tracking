
<h1>About</h1>

I chose to implement all the helper functions manually to ensure reusability and modularity. The main detector is trained using YOLO7 implementation by https://github.com/WongKinYiu/yolov7. The dataset is modified to fit the requirements of the YOLO model. 


<h1>Results</h1>
Result for provided test video in experiments/run1

![](https://github.com/AydamirMirzayev/stroma-tracking/blob/master/result.gif)

<h1>Setup</h1>
As it is conflicting to build the runtime enviroment locally, in this repository we will use the environment by google colab. 
However, to keep the code modular and reusable. Background operations of the network are build on locally tested .py files 
and can be easily integrated into locally or clound run application. To run the program: 

Naviage to GoogleDriveEnvironmentSetup.ipynb and follow instructions for environment setup and inference

<h1>Inference</h1>

After initial setup navigate to Inference.ipynb

<h3>Data analysis</h3> 
In: analyze_data.ipynb

In notebook analyze_data check the distribution of the labels in the dataset as well as video format.

<h3>Frame exraction</h3> 
In: extract_frames.py

For the first set of experiments I decided to use every 10th frame. (3fps)
Frames are exracted using ffmpeg library and python scripting

<h3>COCO to YOLO conversion</h3>
In: json2yolo7.py

Converting COCO labeling to YOLO labeling for each frame.

<h3>Object Counting</h3>

Centroid Tracker Class adapted from 
https://pyimagesearch.com/2018/07/23/simple-object-tracking-with-opencv/

Following improvement have beed made on the class to customize it for the task at hand 

1) Before registering new object it is first added to a waitlist and tracked for a minimum of 
    'minCandidateFrames' to ensure that noisy detections are not counted.

2) Since objects are falling from the top we add an additional protection agaist noise and ensure that obects pass
    a user-set treshold of 'maxDist' before registering the object and incrementing the count 

3) LowerTreshold is for future update where objects are marked as deregistered (left the frame) if they are below a 
    certain treshold in the frame. 

4) A treshold of maximum distance (maxDist) is introduced to ensure that two objects that are close are not matched to each other

Later count_objects.py script is implemented that accepts set of video frames and corresponding labels and otpusts a set of frames with counts 
imprinted on top

<h3>Reconstructing video from frames</h3>
In: reconstruct_video.py

Converting individual frames to VIDEO .mp4 format.

<h3>Predict on video</h3>
In: predict_on_video.py

Bringing all the individual pieces together to convert input test video to a tracked video.


<h3>To do</h3>

Update the counding for missing objects

