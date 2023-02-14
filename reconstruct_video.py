""" Converter for individual frames to the final video
	: reconstruct video [-h] frame_dir, labels_dir, out_path

Covert frames to videos with detection boxes

positional arguments:
  frame_dir   Path to the directory with input frames
  labels_dir  Path to the prediction labels
  out_path    Path to the output directory

optional arguments:
  -h, --help  show this help message and exit

usage: reconstruct_video.py [in path] [predictions path] [out folder path]
"""
import cv2 
import os
import glob 

def generate_video(frame_dir, labels_dir, out_path):
	out = cv2.VideoWriter(, cv2.)



if __name__ == '__main__':
	parser = argparse.ArgumentParser(
	                    prog = 'Video Generator',
	                    description = 'Covert frames to videos with detection boxes',
	                    epilog = 'usage: reconstruct_video.py [in path] [predictions path] [out folder path]')

	parser.add_argument('frame_dir', help = 'Path to the directory with input frames', type = str)
	parser.add_argument('labels_dir', help = 'Path to the prediction labels', type = int)
	parser.add_argument('out_path', help = 'Path to the output directory', type = str)
	
	args = parser.parse_args()

	convert_tracked_to_video(args.frame_dir, args.labels_dir, args.out_path)
