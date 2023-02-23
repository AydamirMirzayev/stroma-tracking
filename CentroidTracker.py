from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np

class CentroidTracker():
    '''
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
    '''
    def __init__(self, maxDisappeared=10, upperTreshold = 50, lowerTreshold = 50, minCandidateFrames = 10, maxDist = 40):
        # initialize the next unique object ID along with two ordered
        # dictionaries used to keep track of mapping a given object
        # ID to its centroid and number of consecutive frames it has
        # been marked as "disappeared", respectively
        self.nextObjectID = 1
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()
        
        # @aydamir
        self.maxDist = maxDist
        self.candidateObjectID = -1
        self.minCandidateFrames = minCandidateFrames
        self.candidateObjects = OrderedDict()
        self.candidateObjectScores = OrderedDict()
        self.objectCoordinates = OrderedDict() # Add object coordinates

        # store the number of maximum consecutive frames a given
        # object is allowed to be marked as "disappeared" until we
        # need to deregister the object from tracking
        self.maxDisappeared = maxDisappeared
        
        # @aydamir
        self.upperTreshold = upperTreshold
        self.lowerTreshold = lowerTreshold

    def register(self, centroid, coordinates): # ok?
        # when registering an object we use the next available object
        # ID to store the centroid
        
        self.objects[self.nextObjectID] = centroid 
        self.objectCoordinates[self.nextObjectID] = coordinates
        self.disappeared[self.nextObjectID] = 0  # This keeps count of object dissapearance.
        self.nextObjectID += 1
        
    # @aydamir
    def deregister(self, objectID): # ok
        # to deregister an object ID we delete the object ID from
        # both of our respective dictionaries
        del self.objects[objectID]
        del self.disappeared[objectID]
        del self.objectCoordinates[objectID]
    
    # @aydamir
    def add_candidate(self, centroid):
        # when new object enters the scene, instead of adding it as a new object add it as
        # an object candidate and if it stays in for more than N number of frames 
        # register it as a new permament object
        
        self.candidateObjects[self.candidateObjectID] = centroid
        self.candidateObjectScores[self.candidateObjectID] = 1
        self.candidateObjectID -= 1

    # @aydamir
    def remove_candidate(self, objectID):
        # Deregister a candidate object
        
        del self.candidateObjects[objectID]
        del self.candidateObjectScores[objectID]
    
    def update(self, rects): 
        # check to see if the list of input bounding box rectangles
        # is empty
        if len(rects) == 0:
            # loop over any existing tracked objects and mark them
            # as disappeared
            for objectID in list(self.disappeared.keys()):
                self.disappeared[objectID] += 1

                # if we have reached a maximum number of consecutive
                # frames where a given object has been marked as
                # missing, deregister it
                if self.disappeared[objectID] > self.maxDisappeared:
                    self.deregister(objectID)
                    
            # @aydamir
            # Also clear the list of candidate objects 
            for objectID in list(self.candidateObjects.keys()):
                self.remove_candidate(objectID)

            # return early as there are no centroids or tracking info
            # to update
            return self.objects, self.objectCoordinates

        # initialize an array of input centroids for the current frame
        inputCentroids = np.zeros((len(rects), 2), dtype="int")
        inputCoordinates = np.zeros((len(rects), 2), dtype="int")

        # loop over the bounding box rectangles
        for (i, (startX, startY, endX, endY)) in enumerate(rects):
            # use the bounding box coordinates to derive the centroid
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            inputCentroids[i] = (cX, cY)
            inputCoordinates[i] = (startX, startY)

        # if there are currently not any candidate objects 
        # add inputs to the list of candidate objects
        #print(len(self.candidateObjects), len(self.objects))
        if len(self.candidateObjects) == 0 and len(self.objects) == 0:
            for i in range(0, len(inputCentroids)):
                self.add_candidate(inputCentroids[i])

        # otherwise, if we are currently tracking objects we need to
        # try to match the input centroids to existing object
        # centroids
        else:
            # grab the set of object IDs and candidate IDs corresponding centroids
            objectIDs = list(self.objects.keys()) + list(self.candidateObjects.keys())
            objectCentroids = list(self.objects.values()) + list(self.candidateObjects.values())

            # compute the distance between each pair of object
            # centroids and input centroids, respectively -- our
            # goal will be to match an input centroid to an existing
            # object centroid
            D = dist.cdist(np.array(objectCentroids), inputCentroids)

            # in order to perform this matching we must (1) find the
            # smallest value in each row and then (2) sort the row
            # indexes based on their minimum values so that the row
            # with the smallest value as at the *front* of the index
            # list
            rows = D.min(axis=1).argsort()

            # next, we perform a similar process on the columns by
            # finding the smallest value in each column and then
            # sorting using the previously computed row index list
            cols = D.argmin(axis=1)[rows]
    
            # in order to determine if we need to update, register,
            # or deregister an object we need to keep track of which
            # of the rows and column indexes we have already examined
            usedRows = set()
            usedCols = set()

            # loop over the combination of the (row, column) index
            # tuples
            for (row, col) in zip(rows, cols):
                # if we have already examined either the row or
                # column value before, ignore it
                # val
                if row in usedRows or col in usedCols:
                    continue
                    
                if D[row, col] < self.maxDist:
                    usedRows.add(row)
                    usedCols.add(col)
                    continue

                # otherwise, grab the object ID for the current row,
                # set its new centroid, and reset the disappeared
                # counter
                objectID = objectIDs[row]
                
                # @aydamir
                if objectID > 0: # If the object is candidate   
                    #print('get hehehehe')
                    self.objects[objectID] = inputCentroids[col]
                    self.objectCoordinates[objectID] = inputCoordinates[col]
                    self.disappeared[objectID] = 0
                else:
                    
                    
                    print('get here for: ', objectID)
                    self.candidateObjects[objectID] = inputCentroids[col]
                    self.candidateObjectScores[objectID] += 1
                    

                    # If object has been present for more than N number of frames 
                    # Add it to the list of objects

                    print('Object Score: ', self.candidateObjectScores[objectID])
                    print('Object Y coord: ', inputCentroids[col][1])

                    if self.candidateObjectScores[objectID] >= self.minCandidateFrames  and inputCoordinates[col][1] > self.upperTreshold:
                        print('Pass the object')
                        self.register(inputCentroids[col], inputCoordinates[col])
                        self.remove_candidate(objectID)

                # indicate that we have examined each of the row and
                # column indexes, respectively
                usedRows.add(row)
                usedCols.add(col)

            # compute both the row and column index we have NOT yet
            # examined
            unusedRows = set(range(0, D.shape[0])).difference(usedRows)
            unusedCols = set(range(0, D.shape[1])).difference(usedCols)

            # in the event that the number of object centroids is
            # equal or greater than the number of input centroids
            # we need to check and see if some of these objects have
            # potentially disappeared
            if D.shape[0] >= D.shape[1]:
                # loop over the unused row indexes
                for row in unusedRows:
                    # grab the object ID for the corresponding row
                    # index and increment the disappeared counter
                    objectID = objectIDs[row]
                    
                    if objectID > 0:
                        self.disappeared[objectID] += 1
                        # check to see if the number of consecutive
                        # frames the object has been marked "disappeared"
                        # for warrants deregistering the object
                        if self.disappeared[objectID] > self.maxDisappeared:
                            self.deregister(objectID)
                    else:
                        self.remove_candidate(objectID)

            # otherwise, if the number of input centroids is greater
            # than the number of existing object centroids we need to
            # register each new input centroid as a trackable object
            else:
                for col in unusedCols:
                    self.add_candidate(inputCentroids[col])
                    #self.register(inputCentroids[col])

        # return the set of trackable objects
        return self.objects, self.objectCoordinates