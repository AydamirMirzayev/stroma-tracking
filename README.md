
<h1>About</h1>

I chose to implement all the helper functions manually to ensure reusability and modularity. The main detector is trained is trained using YOLO7 implementation by https://github.com/WongKinYiu/yolov7. The dataset is modified to fit the requirements of the YOLO model. 


<h1>Setup</h1>

As it is conflicting to build the runtime enviroment locally, in this repository we will use the environment by google colab. 
However, to keep the code modular and reusable. Background operations of the network are build on locally tested .py files 
and can be easily integrated into locally or clound run application. To run the program: 

 Markup : * Installing necessary repositories
 				* Naviage to StromaInference.ipynb and follow instructions for environment setup and inference

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

<h3>Reconstructing video from frames</h3>
In: reconstruct_video.py

Converting individual frames to VIDEO .mp4 format.

<h3>Predict on video</h3>
In: predict_on_video.py

Bringing all the individual pieces together to convert input test video to a tracked video.


