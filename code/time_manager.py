import time
import threading 
import datetime
import os
import gui_config

data_path = os.path.dirname(os.path.abspath(__file__)) + '/../'
    
if gui_config.DEVELOPER_MODE :
    data_path += '.local_debug/'
else :
    data_path += '.local/'

RESET_DAY_FILE = data_path + 'reset_day'
CURRENT_WEEK_START_DATE_FILE = data_path + 'current_week_start_date' 




class TimeManager( object ) :

    def __init__( self, task_manager, task_table ) :

        self.task_manager = task_manager
        self.task_table = task_table

        self.check_time()
        
        cron_check_time_thread = threading.Thread( target = self.cron_check_time_target,
                                                   daemon = 1 )
        cron_check_time_thread.start() 
        


    def check_time( self ) :

        today = datetime.date.today()

        # day, month, year = today.day, today.month, today.year
        
        current_week_datetime = self.read_current_start_week() 

        # days, seconds, microseconds
        diff = today - current_week_datetime 

        if diff.days > 7 :

            self.write_current_start_week( today )

            self.task_manager.clear_progress()

            self.task_table.reload() 



    def read_current_start_week( self ) :

        with open( CURRENT_WEEK_START_DATE_FILE, 'r' ) as f :
            current_week_start_date = f.read() 

        current_week_datetime = datetime.datetime.strptime( current_week_start_date,
                                                            '%Y-%m-%d' ).date() 
        return current_week_datetime 


    
    # accepts today datetime and writes to disk 
    def write_current_start_week( self, today ) :


        today_weekday = today.weekday() 

        # 0 = monday, ..., 6 = sunday 
        with open( RESET_DAY_FILE, 'r' ) as f :
            reset_day = int( f.read() ) 

        # most recent date with that day 
        new_start_week_date = today - datetime.timedelta( 7 + today_weekday - reset_day )

        new_start_week_date_str = new_start_week_date.strftime( '%Y-%m-%d' )
        
        # print( new_start_week_date_str ) 
        
        with open( CURRENT_WEEK_START_DATE_FILE, 'w' ) as f :
            f.write( new_start_week_date_str ) 


        
    def cron_check_time_target( self ) :

        while( 1 ) :
            self.check_time()
            time.sleep( 300  )
            

        
