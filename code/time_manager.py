import time
import threading 
import datetime
import os
import numpy as np 
# import h5py

import gui_config


WEEKLY_RESET_DAY_FILE = gui_config.data_path + 'weekly_reset_day'
# CURRENT_WEEK_START_DATE_FILE = data_path + 'current_week_start_date' 
LAST_USED_DATE_FILE = gui_config.data_path + 'last_used_date.txt'




class TimeManager( object ) :

    # list of datetimes 
    reset_dates = None
    weekly_reset_day = 5  # saturday = default 
    
    # these are both datetime 
    today = None
    last_used_date = None

    
    def __init__( self, controller ) :
        self.controller = controller

        
        
    def init( self ) : 

        self.task_manager = self.controller.task_manager
        self.task_table = self.controller.task_table

        self.reset_dates = np.zeros( gui_config.NUM_TIMESCALES, dtype = object ) 

        self.today = datetime.date.today()

        self.read_weekly_reset_day()
        self.read_last_used_date()

        self.compute_reset_dates() 
        
        self.check_time()

        self.write_last_used_date()
        
        # cron_check_time_thread = threading.Thread( target = self.cron_check_time_target,
        #                                            daemon = 1 )
        # cron_check_time_thread.start() 

        

    # reset data if a day, week, month, quarter, or year is exceeded
    
    def check_time( self ) :
        for i in range( gui_config.NUM_TIMESCALES ) :

            print( self.reset_dates[i] )
                
            if self.today >= self.reset_dates[i] :
                self.task_manager.clear_progress( i )


        
    # 0 = monday, ..., 6 = sunday     
    def read_weekly_reset_day( self ) :
        try : 
            with open( WEEKLY_RESET_DAY_FILE, 'r' ) as f :
                self.weekly_reset_day = int( f.read() )

        except :
            self.write_weekly_reset_day()

            
    def write_weekly_reset_day( self ) : 
        with open( WEEKLY_RESET_DAY_FILE, 'w' ) as f :
            f.write( str( self.weekly_reset_day ) )

            
            

    
    def read_last_used_date( self ) :
        try : 
            with open( LAST_USED_DATE_FILE, 'r' ) as f :
                date_str = f.read() 
            self.last_used_date = datetime.datetime.strptime( date_str, '%Y-%m-%d' ).date() 

        except :
            self.write_last_used_date()
            self.last_used_date = self.today

    
    
    # accepts today datetime and writes to disk 
    def write_last_used_date( self ) :

        date_str = self.today.strftime( '%Y-%m-%d' )

        with open( LAST_USED_DATE_FILE, 'w' ) as f :
            f.write( date_str ) 

            

    def compute_reset_dates( self ) :

        self.reset_dates[0] = self.last_used_date + datetime.timedelta( 1 )



        # find next date with the same day as reset_day 
        diff = self.weekly_reset_day - self.last_used_date.weekday()
        if diff < 0 :
            diff += 7
        
        # new_start_week_date = today - datetime.timedelta( 7 + today_weekday - self.reset_day )
        self.reset_dates[1] = self.last_used_date + datetime.timedelta( days = diff )


        # find next month
        month = self.last_used_date.month
        year = self.last_used_date.year
        
        if month == 12 :
            nextmonth_month = 1
            nextmonth_year = year + 1
        else :
            nextmonth_month = month + 1
            nextmonth_year = year 
                    
        self.reset_dates[2] = datetime.date( year = nextmonth_year,
                                             month = nextmonth_month,
                                             day = 1  )

        # compute next quarter
        if month >= 10 :
            nextquarter_month = 1
            nextquarter_year = year + 1

        else :
            if month % 3 == 0 : 
                nextquarter_month = month + 1
            else :
                nextquarter_month = month + 3 - month % 3 + 1
                
            nextquarter_year = year 
        
        self.reset_dates[3] = datetime.date( year = nextquarter_year,
                                             month = nextquarter_month,
                                             day = 1 )

        # year
        self.reset_dates[4] = datetime.date( year = self.last_used_date.year + 1,
                                             month = 1,
                                             day = 1 )

                    
        
    def cron_check_time_target( self ) :

        while( 1 ) :
            self.check_time()
            time.sleep( 300  )
            

        
