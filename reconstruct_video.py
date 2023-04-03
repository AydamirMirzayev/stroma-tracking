""" Converter for individual frames to the final video
	: reconstruct video [-h] frame_dir, out_path

Covert frames to videos with detection boxes

positional arguments:
  frame_dir   Path to the directory with input frames
  out_path    Path to the output directory

optional arguments:
  -h, --help  show this help message and exit

usage: reconstruct_video.py [in path] [out folder path]
"""

import cv2 
import glob 
import argparse
from constants import IM_WIDTH, IM_HEIGHT, FILENAME_LENGTH, IMAGE_FORMAT

fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

def generate_video(frame_dir, out_path, fps = 10, out_filename = 'tracked_recording.mp4'):
	# Get the names of all the frames
	frames = [path[-FILENAME_LENGTH:] for path in glob.glob(f'{frame_dir}/*{IMAGE_FORMAT}')]

	out = cv2.VideoWriter(f'{out_path}/{out_filename}', fourcc, fps, (IM_WIDTH, IM_HEIGHT))

	# List all the image files in the folder 
	for filename in frames:
		image = cv2.imread(f'{frame_dir}/{filename}')
		out.write(image)

	out.release()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
	                    prog = 'Video Generator',
	                    description = 'Covert frames to videos with detection boxes',
	                    epilog = 'usage: reconstruct_video.py [in path] [predictions path] [out folder path]')

	parser.add_argument('frame_dir', help = 'Path to the directory with input frames', type = str)
	parser.add_argument('out_path', help = 'Path to the output directory', type = str)
	parser.add_argument('fps', help = 'FPS of the video file to be generated', default = 10)
	parser.add_argument('out_file', help = 'The name of the output file, with extension included', default = 'tracked_recording.mp4')

	args = parser.parse_args()

	print('Processing...')
	generate_video(args.frame_dir, args.out_path, args.fps, args.out_file)
	print('Done.')
