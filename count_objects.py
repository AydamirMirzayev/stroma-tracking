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
WRITE_OFFSET = 5
BOLT_X = 20
NUT_X = 20
BOLT_Y = 20
NUT_Y = 40

# Given a set of YOLO coordinates converts them to a set of COCO coordinates
def convert_yolo_to_COCO(bbox, imHeight, imWidth):
    COCO_bbox = []
    
    xCenter = bbox[0]
    yCenter = bbox[1]
    width = int(round(bbox[2]*imWidth))
    height = int(round(bbox[3]*imHeight))
    
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
        
        label = int(line[0])
        bbox = []
        for cor in line[2:].split(' '):
            bbox.append(float(cor))
        bbox = convert_yolo_to_COCO(bbox, 640, 640)
            
        if label == 0:
            boltCoordinates.append(bbox)
            boltLabels.append(label)
        else:
            nutCoordinates.append(bbox)
            nutLabels.append(label)
        
    data = {}
    
    data['bolt_labels'] = boltLabels
    data['bolt_bboxes'] = boltCoordinates
    data['nut_labels'] = nutLabels
    data['nut_bboxes'] = nutCoordinates
         
    return data

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

    # Create centroid tracker objects
    nutCentroids = ct.CentroidTracker(maxDisappeared=args.maxGone, upperTreshold = args.topTresh, lowerTreshold = args.lowTresh, minCandidateFrames = args.minCandFrames, maxDist = args.maxDist)
    boltCentroids = ct.CentroidTracker(maxDisappeared=args.maxGone, upperTreshold = args.topTresh, lowerTreshold = args.lowTresh, minCandidateFrames = args.minCandFrames, maxDist = args.maxDist)
    
    # Keep track of maximum number of objects
    numOfBolts = 0
    numOfNuts = 0

    # Process every frame in the video
    files = [path[-8:] for path in glob.glob( f'{args.framesPath}/*.jpg')]

    for file in files:
        # Get the name of the image file and read it
        name = file.split('.')[0]
        frame = cv2.imread(f'{args.framesPath}/{name}.jpg')

        # Check if there are any object coordinates for that object 
        if os.path.exists(f'{args.labelsPath}/{name}.txt'):

            # Read the text file containing the labels for the current frame
    	    with open( f'{args.labelsPath}/{name}.txt') as f:
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
                cv2.putText(frame, objectText, (boltCoord[0] - WRITE_OFFSET, boltCoord[1]- WRITE_OFFSET), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    	        
    	    for i, (objectID, centroid) in enumerate(nuts.items()):
    	        if objectID > numOfNuts:
    	            numOfNuts = objectID
    	        
    	        objectText = "Nut:  {}".format(objectID)
    	        nutCoord = nutCoords[objectID]
    	        cv2.putText(frame, objectText, (nutCoord[0] - WRITE_OFFSET, nutCoord[1]- WRITE_OFFSET), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Update the text on the frames
        mainBoltText = "Bolts: {}".format(numOfBolts)
        mainNutText = "Nuts: {}".format(numOfNuts)

        # Update Object count on the frames
        cv2.putText(frame, mainNutText, (BOLT_X, BOLT_Y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(frame, mainBoltText, (NUT_X, NUT_Y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Write the updated frame to the target folder
        cv2.imwrite(f'{args.targetFramePath}/{name}.jpg', frame)