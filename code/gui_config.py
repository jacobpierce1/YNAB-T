import os 
import sys 


DEVELOPER_MODE = 0

# dimensions of the gui main window in pixels 
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600 



NUM_TIMESCALES = 5

DEFAULT_NUM_TRANSACTIONS = 10


if len( sys.argv ) > 1 : 
    if sys.argv[1] == 'debug' : 
        DEVELOPER_MODE = 1


data_path = os.path.dirname(os.path.abspath(__file__)) + '/../'

if DEVELOPER_MODE :
    data_path += '.local_debug/'
else :
    data_path += '.local/'
