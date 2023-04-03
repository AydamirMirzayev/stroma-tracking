"""
usage: count_objects.py [-h] [--maxGone MAXGONE] [--topTresh TOPTRESH] [--lowTresh LOWTRESH] [--minCandFrames MINCANDFRAMES] [--maxDist MAXDIST]
                        labelsPath framesPath targetFramePath

Count objects from the bounding bouxes using CentroidTracker

positional arguments:
  labelsPath           Path to the directory with the label files
  framesPath           Path to the directory with frame image files
  targetFramePath     Path to the output directory for the image frames

optional arguments:
  -h, --help            show this help message and exit
  --maxGone MAXGONE     Maximum number of frames before object considered not present
  --topTresh TOPTRESH   Top treshold which object needs to pass to be registered and counted
  --lowTresh LOWTRESH   Lower Treshold after which object is deregistered and no longer tracked
  --minCandFrames MINCANDFRAMES
                        Minimum number of frames object needs to be present to be registered and added to the list
  --maxDist MAXDIST     Maximum distance (pixels) it is plausible for an object to move between frames
"""
import os
import cv2
import glob
import argparse
import CentroidTracker as ct

# Define constants for various offsets in text printing for the 
# Image dimension constants
IM_WIDTH = 640
IM_HEIGHT = 640

# Coordiate constrants
NUT_TEXT_COORD = (20, 40)
BOLT_TEXT_COORD = (15, 20)
BACKGROUND_START_COORD = (5, 2)
BACKGROUND_END_COORD = (115, 47)

# Design constants
Y_OFFSET_COUNT = 15
BACKGROUND_THICKNESS = -1
TOP_TEXT_COLOR = (256, 256, 256)
INPLACE_TEXT_COLOR = (0, 255, 0)
BACKGROUND_COLOR_BGR = (148, 83, 11)
TOP_FONT_SCALE = 1
TOP_FONT_THICK = 1
INP_FONT_SCALE = 1 
INP_FONT_THICK = 1


# Index coordinate constants and string constants 
FILENAME_LENGTH = 8
X_IND = 0 # Index for x coordinate
Y_IND = 1 # Index for y coordinate 
WIDTH_IND = 2
HEIGHT_IND = 3
LABEL_INDEX = 0
COORD_INDEX = 2

# LABEL CONSTANTS
BOLT_LABEL = 0
NUT_LABEL = 1

# Given a set of YOLO coordinates converts them to a set of COCO coordinates
def convert_yolo_to_COCO(bbox, imHeight, imWidth):
    COCO_bbox = []
    
    xCenter = bbox[X_IND]
    yCenter = bbox[Y_IND]
    width = int(round(bbox[WIDTH_IND]*imWidth))
    height = int(round(bbox[HEIGHT_IND]*imHeight))
    
    xmin = (xCenter*2*imWidth - width)/2
    xmin = int(round(xmin))
    ymin = (yCenter*2*imHeight - height)/2
    ymin = int(round(ymin))

    COCO_bbox.append(xmin)
    COCO_bbox.append(ymin)
    COCO_bbox.append(xmin + width)
    COCO_bbox.append(ymin + height)

    return COCO_bbox

# Given contents of a txt file in the YOLO output format returns a COCO-like set of bounding box coordinates 
def get_labels_coordinates(lines):
    nutLabels = []
    nutCoordinates = []
    
    boltLabels = []
    boltCoordinates = []

    for line in lines:
        
        label = int(line[LABEL_INDEX]) 
        bbox = []
        for cor in line[COORD_INDEX:].split(' '):
            bbox.append(float(cor))
        bbox = convert_yolo_to_COCO(bbox, IM_HEIGHT, IM_WIDTH)
            
        if label == BOLT_LABEL:
            boltCoordinates.append(bbox)
            boltLabels.append(label)
        elif label == NUT_LABEL:
            nutCoordinates.append(bbox)
            nutLabels.append(label)
        
    data = {}
    
    data['bolt_labels'] = boltLabels
    data['bolt_bboxes'] = boltCoordinates
    data['nut_labels'] = nutLabels
    data['nut_bboxes'] = nutCoordinates
         
    return data

# Main functionality of the module
def count_objects(labelsPath, framesPath, targetFramePath, maxDisappeared=5,\
    upperTreshold = 50, lowerTreshold = 20, minCandidateFrames = 5, maxDist = 40):

    # Create centroid tracker objects
    nutCentroids = ct.CentroidTracker(maxDisappeared, upperTreshold, lowerTreshold, minCandidateFrames, maxDist)
    boltCentroids = ct.CentroidTracker(maxDisappeared, upperTreshold, lowerTreshold, minCandidateFrames, maxDist)
    
    # Keep track of maximum number of objects
    numOfBolts = 0
    numOfNuts = 0

    # Process every frame in the video
    files = [path[-FILENAME_LENGTH:] for path in glob.glob( f'{framesPath}/*.jpg')]

    for file in files:
        # Get the name of the image file and read it 
        name = file.split('.')[0]   # Obtain first half of the filanme to obtain the name witout file extension                                                
        frame = cv2.imread(f'{framesPath}/{name}.jpg')

        # Check if there are any object coordinates for that object 
        if os.path.exists(f'{labelsPath}/{name}.txt'):

            # Read the text file containing the labels for the current frame
    	    with open( f'{labelsPath}/{name}.txt') as f:
    	        labelLines = f.readlines()
    	    f.close()
    	    
            # Convert format in the files to the set of bouding boxes and labels
            # Update the object locations from tracked objects
    	    trackedObjects = get_labels_coordinates(labelLines) 
    	    bolts, boltCoords = boltCentroids.update(trackedObjects['bolt_bboxes'])
    	    nuts, nutCoords = nutCentroids.update(trackedObjects['nut_bboxes'])


            # Go over updated bouding boxes and update the number of total objects accordingly
            # Update the count locations on the frames
    	    for i, (objectID, centroid) in enumerate(bolts.items()):
                if objectID > numOfBolts:
                   numOfBolts = objectID

                objectText = "Bolt: {}".format(objectID)
                boltCoord = boltCoords[objectID]
                cv2.putText(frame, objectText, (boltCoord[X_IND], boltCoord[Y_IND]- Y_OFFSET_COUNT), \
                    cv2.FONT_HERSHEY_SIMPLEX, INP_FONT_SCALE, INPLACE_TEXT_COLOR, INP_FONT_THICK)
    	        
    	    for i, (objectID, centroid) in enumerate(nuts.items()):
    	        if objectID > numOfNuts:
    	            numOfNuts = objectID
    	        
    	        objectText = "Nut:  {}".format(objectID)
    	        nutCoord = nutCoords[objectID]
    	        cv2.putText(frame, objectText, (nutCoord[X_IND], nutCoord[Y_IND]- Y_OFFSET_COUNT), \
                    cv2.FONT_HERSHEY_SIMPLEX, INP_FONT_SCALE, INPLACE_TEXT_COLOR, INP_FONT_THICK)
        
        # Update the text on the frames
        mainBoltText = "Bolts:{}".format(numOfBolts)
        mainNutText = "Nuts:{}".format(numOfNuts)

        # Update Object count on the frames
        cv2.rectangle(frame, BACKGROUND_START_COORD, BACKGROUND_END_COORD, BACKGROUND_COLOR_BGR, BACKGROUND_THICKNESS)
        cv2.putText(frame, mainBoltText, BOLT_TEXT_COORD, cv2.FONT_HERSHEY_COMPLEX_SMALL, TOP_FONT_SCALE, TOP_TEXT_COLOR, TOP_FONT_THICK)
        cv2.putText(frame, mainNutText, NUT_TEXT_COORD, cv2.FONT_HERSHEY_COMPLEX_SMALL, TOP_FONT_SCALE, TOP_TEXT_COLOR, TOP_FONT_THICK)
        

        # Write the updated frame to the target folder
        cv2.imwrite(f'{targetFramePath}/{name}.jpg', frame)


if __name__ == '__main__':
    #Create a parser
    parser = argparse.ArgumentParser(description='Count objects from the bounding bouxes using CentroidTracker')

    parser.add_argument('labelsPath', help = 'Path to the directory with the label files', type = str)
    parser.add_argument('framesPath', help = 'Path to the directory with frame image files', type = str)
    parser.add_argument('targetFramePath', help = 'Path to the output directory for the image frames', type = str)
    parser.add_argument('--maxGone', default=5, help='Maximum number of frames before object considered not present')
    parser.add_argument('--topTresh', default=50, help='Top treshold which object needs to pass to be registered and counted')
    parser.add_argument('--lowTresh', default=20, help='Lower Treshold after which object is deregistered and no longer tracked')
    parser.add_argument('--minCandFrames', default = 5, help='Minimum number of frames object needs to be present to be registered and added to the list')
    parser.add_argument('--maxDist', default =40, help='Maximum distance (pixels) it is plausible for an object to move between frames')

    args = parser.parse_args()

    count_objects(args.labelsPath, args.framesPath, args.targetFramePath,\
    args.maxGone, args.topTresh, args.lowTresh, args.minCandFrames, args.maxDist)

