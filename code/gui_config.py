import os 

DEVELOPER_MODE = 1

# dimensions of the gui main window in pixels 
WINDOW_WIDTH = 950
WINDOW_HEIGHT = 600 



NUM_TIMESCALES = 5


data_path = os.path.dirname(os.path.abspath(__file__)) + '/../'


if DEVELOPER_MODE :
    data_path += '.local_debug/'
else :
    data_path += '.local/'
