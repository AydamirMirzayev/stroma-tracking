<h3>Frame exraction</h3> 
Frames are exracted using ffmpeg library at 3fps (Every 10th frame)

[Faster Way] use the command below and then remane frame names since ffmpeg does not allow filename formatting. 

ffmpeg -i ./images/test/test.mp4 -vf "select=not(mod(n\,10))" -vsync vfr ./frames/test/test_frame_%03d.png

python extract_frames.py ./data/images/test/test.mp4 10 ./data/frames/test test_frame

