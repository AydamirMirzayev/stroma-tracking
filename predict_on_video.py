import os
import sys
import argparse
import extract_frames
import reconstruct_video

EXPERIMENT_LIMIT = 100
DETECT_FILE = './yolov7/detect.py'
WEIGHTS = './best.pt'
CONFIDENCE_INTERVAL = 0.2

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
	                    prog = 'Predictor',
	                    description = 'Running predictions on a test video',
	                    epilog = 'usage: predict_on_video.py [source_video]')

	parser.add_argument('source_video', help = 'Path to the video source', type = str)
	args = parser.parse_args()

	# Create the directory tree for the run 
	experiment_id = 1
	try: 
		if not os.path.exists('./experiments'):
			os.mkdir('./experiments')	

		while experiment_id < EXPERIMENT_LIMIT:
			if not os.path.exists(f'./experiments/run{experiment_id}'):
				os.mkdir(f'./experiments/run{experiment_id}')
				print(f"Experiments in: experiments/run{experiment_id}")
				
				os.mkdir(f'./experiments/run{experiment_id}/video_frames')
				os.mkdir(f'./experiments/run{experiment_id}/results')
				break

			else:
				experiment_id = experiment_id + 1

	except:
		print('ERROR creating experiment tree')
		sys.exit()

	#Extract the video frames to directory
	print('Extracting frames...')
	extract_frames.extract_selected_frames(args.source_video, 1, f'./experiments/run{experiment_id}/video_frames')
	print('\n Extracting frames: Done.')

	# Call prediction method
	print('Running predictions....')
	os.system(f'python {DETECT_FILE} --weights {WEIGHTS} --conf {CONFIDENCE_INTERVAL} --source ./experiments/run{experiment_id}/video_frames')
	print('\n Running predictions: Done.')

	# Reassemble the video back. 
	print('Reassembling video...')
	reconstruct_video.generate_video('./yolov7/runs/detect/exp', f'./experiments/run{experiment_id}/results') 
	print('\n Reassembling video: Done.')



