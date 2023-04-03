# Video and image parameters dimension constants
IM_WIDTH = 640
IM_HEIGHT = 640
FPS = 10
IMAGE_FORMAT = '.jpg'

# Index coordinate constants and string constants 
FILENAME_LENGTH = 8
X_IND = 0 # Index for x coordinate in coordinate tuples
Y_IND = 1 # Index for y coordinate in coordinate tuples
WIDTH_IND = 2 # Index for with in bounding box
HEIGHT_IND = 3 # Index for height in bounding box 
LABEL_INDEX = 0 # Index of the label in YOLO label string 
COORD_INDEX = 2 # Starting index for coordinates in YOLO label string

# Label constants
BOLT_LABEL = 0 # Label used for the bolt
NUT_LABEL = 1 # Label used for the nut 

# Styling constants used for drawing on resulting frames
# Frame Drawing constants
NUT_TEXT_COORD = (20, 40)	# Coordiate for the text 'Nuts' in top left
BOLT_TEXT_COORD = (15, 20)	# Coordinate for the text 'Bolts' in the top 
BACKGROUND_START_COORD = (5, 2)		# Starting coordinates for background rectangle in top Left
BACKGROUND_END_COORD = (115, 47)	# Ending coordinate for top left rectangle
Y_OFFSET_COUNT = 15	# Y coordinate offset for in place object count text
BACKGROUND_THICKNESS = -1	# Thickness parameter for the background rectange (-1 = fill)
TOP_TEXT_COLOR = (256, 256, 256) # Color for the text at the top left 
INPLACE_TEXT_COLOR = (0, 255, 0) # Color for the in place object count text
BACKGROUND_COLOR_BGR = (148, 83, 11) # Color for the top left background rectangle
TOP_FONT_SCALE = 1 # Scale parameter for the top text 
TOP_FONT_THICK = 1 # Thickness parameter for the top text
INP_FONT_SCALE = 0.5 # Scale parameter for in place text 
INP_FONT_THICK = 2 # Font thickness for in place text

