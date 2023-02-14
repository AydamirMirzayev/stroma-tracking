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

WIDTH = 640 
HEIGHT = 640 
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
FPS = 30

def generate_video(frame_dir, out_path):
	# Get the names of all the frames
	frames = [path[-8:] for path in glob.glob(f'{frame_dir}/*.jpg')]

	out = cv2.VideoWriter(f'{out_path}/tracked_recording.mp4', fourcc, FPS, (WIDTH, HEIGHT))

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

	args = parser.parse_args()

	print('Processing...')
	generate_video(args.frame_dir, args.out_path)
	print('Done.')
