import os 
import extract_frames

EXPERIMENT_LIMIT = 100

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
	                    prog = 'Predictor',
	                    description = 'Running predictions on a test video',
	                    epilog = 'usage: predict_on_video.py [source_video]')

	parser.add_argument('source_video', help = 'Path to the video source', type = str)
	experiment_id = 1

	# Create the directory tree for the run 
	try: 
		if not os.path.exists('./experiments'):
			os.path.mkdir('./experiments')	

		while experiment_id < EXPERIMENT_LIMIT:
			if not os.path.exists(f'.experiments/run{experiment_id}'):
				os.path.mkdir(f'.experiments/run{experiment_id}')
				print("Experiments in: experiments/run{experiment_id}")
				
				os.path.mkdir(f'.experiments/run{experiment_id}/video_frames')
				os.path.mdkir(f'.experiments/run{experiment_id}/results')
				break

			else:
				experiment_id = experiment_id + 1

	except:
		print('ERROR creating experiment tree')

	# Extract the video frames to directory
	extract_frames.extract_selected_frames(args.source_video, 1, f'.experiments/run{experiment_id}/video_frames')

	# Call prediction method
	print('predictions....')

	# Reassemble the video back. 