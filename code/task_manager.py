import os 
import threading
import time
import h5py
import numpy as np 
import sys
# import threading 

import gui_config




# CURRENT_TASKS_FILE = data_path + 'active_tasks.txt'

# count the accumulated time for each timescale in this file. at least
# until we introduce transactions.
CURRENT_PROGRESS_FILE = gui_config.data_path + 'current_progress.hdf5'



EXCESS_GOOD, EXCESS_BAD, EXCESS_NEUTRAL = [ 0, 1, 2 ] 



# class Task( object ) :
    
#     def __init__( self, task_name, allocation = 0,
#                   usage = 0, policy = EXCESS_NEUTRAL ) :

#         self.name = task_name
#         self.allocation = allocation
#         self.usage = usage
#         self.policy = policy
        

    # def to_string( self ) :
    #     return '%s\t%.1f\t%.2f\t%d' % ( self.name, self.allocation,
    #                                     self.usage, self.policy )
        
    
    # @classmethod
    # def from_string( cls, s ) :
    #     tmp = [ t(x) for t,x in zip( [ str, float, float, int ],
    #                                  s.split( '\t' ) ) ] 
    #     task_name, allocation, usage, policy = tmp
    #     return cls( task_name, allocation, usage, policy ) 




    
    
class TaskManager( object ) :

    # active_tasks = None
    needs_save = 0
    
    def __init__( self, controller ) :

        self.controller = controller 
        # self.load_active_tasks()
        # mode: read / write if exists, else create 
        self.current_progress_file = h5py.File( CURRENT_PROGRESS_FILE, 'a' )

        # self.lock = threading.Lock()
            
        # cron = threading.Thread( target = self.cron_save_active_tasks,
        #                                                   daemon = 1 )
        # cron.start() 

    def init( self ) :
        pass 
        

    def close( self ) :
        self.current_progress_file.close() 
    
        

    def add_task( self, task_name ) :
        grp = self.current_progress_file.create_group( task_name )

        dset = grp.create_dataset( 'budgeted', ( gui_config.NUM_TIMESCALES, ), dtype = float )
        dset = grp.create_dataset( 'usage', ( gui_config.NUM_TIMESCALES, ), dtype = float )
        dset = grp.create_dataset( 'policy', ( gui_config.NUM_TIMESCALES, ), dtype = float )
        dset = grp.create_dataset( 'row', (1,), dtype = float )

        z = np.zeros( gui_config.NUM_TIMESCALES ) 

        self.current_progress_file[ task_name ][ 'budgeted' ][...] = z
        self.current_progress_file[ task_name ][ 'usage' ][...] = z
        self.current_progress_file[ task_name ][ 'policy' ][...] = z

        row = len( self ) - 1 
        print( 'adding row: ' + str( row ) ) 
        self.current_progress_file[ task_name ][ 'row' ][...] = row 
        
        #        self.set_row( task_name, len( self ) )
                           

    def delete_task( self, task_name ) :
        try : 
            del self.current_progress_file[ task_name ]
        except :
            print( 'ERROR: unable to delete task.' ) 
            
        
    def set_budgeted( self, task_name, budgeted, timescale ) :
        try :
            # with self.lock : 
            self.current_progress_file[ task_name ][ 'budgeted' ][ timescale ] = budgeted
        except :
            print( 'ERROR: unable to set budgeted amount.' ) 

        
    def get_budgeted( self, task_name, timescale ) :
        try :
            return self.current_progress_file[ task_name ][ 'budgeted' ][ timescale ]
        except :
            print( 'ERROR: unable to get budgeted amount.' ) 

            
    def set_usage( self, task_name, usage, timescale ) : 
        try :
            # with self.lock : 
            self.current_progress_file[ task_name ][ 'usage' ][ timescale ] = usage
        except :
            print( 'ERROR: program crash, error setting usage' )
            sys.exit(0)
            
            
    def set_usages( self, task_name, usages ) : 
        try :
            #with self.lock : 
            self.current_progress_file[ task_name ][ 'usage' ][:] = usages
        except :
            print( 'ERROR: program crash, error setting usages for task: ' + task_name )
            sys.exit(0)

            
    def get_usage( self, task_name, timescale ) :
        # print( 'get usage: task_name = ' + str( task_name ) + ' timescale = ' + str( timescale ) )
        try : 
            return self.current_progress_file[ task_name ][ 'usage' ][ timescale ]
        except :
            print( 'ERROR: unable to get usage.' )

            
    def get_usages( self, task_name ) :
        # print( 'get usage: task_name = ' + str( task_name ) + ' timescale = ' + str( timescale ) )
        try : 
            return self.current_progress_file[ task_name ][ 'usage' ][:]
        except :
            print( 'ERROR: unable to get usages.' ) 
        
        
    def set_policy( self, task_name, policy, timescale = None ) :
        try :
            # with self.lock : 
            self.current_progress_file[ task_name ][ 'policy' ][:] = policy 
        except :
            print( 'ERROR: unable to set policy.' ) 

            
    def get_policy( self, task_name, timescale ) :
        try : 
            return self.current_progress_file[ task_name ][ 'policy' ][ timescale ] 
        except :
            print( 'ERROR: unable to get policy.' ) 

            
    def set_row( self, task_name, row, use_lock = 0 ) :
        try :
            # if use_lock : 
            # self.lock.acquire() 

            self.current_progress_file[ task_name ][ 'row' ][0] = row

            # if use_lock : 

        except :
            print( 'ERROR: unable to set row.' ) 

            
    def get_row( self, task_name ) :
        try : 
            return self.current_progress_file[ task_name ][ 'row' ][0]
        except :
            print( 'ERROR: unable to get row.' )
            
        
    def get_task_names( self ) :
        return self.current_progress_file.keys()
 
    
    
    def get_rows( self ) :
        return { key : self.current_progress_file[ task_name ][ 'row' ][0]
                 for key in self.current_progress_file }


    def set_rows( self, rows_dict ) :
        for task_name, row in rows_dict.items() :
            self.set_row( task_name, row ) 
            # self.current_progress_file[ key ][ 'row' ] = row
        

    # todo: recompute current progress from database. debug feature, but ideally
    # will be integrated with the app.
    def synchronize_database( self ) :
        ...

    
    def __len__( self ) :

        if len( self.current_progress_file ) is None :
            return 0

        return len( self.current_progress_file )
    
        
        
    # def load_active_tasks( self ) :

    #     self.active_tasks = []
        
    #     with open( CURRENT_TASKS_FILE, 'r' ) as f :
    #         for line in f.readlines() :
    #             self.active_tasks.append( Task.from_string( line ) )
                
                
                
    # def save_active_tasks( self ) :

    #     print( 'task_manager.py: saving active tasks' ) 

    #     data_str = ''

    #     for i in range( len( self.active_tasks ) ) :
    #         task = self.active_tasks[i] 
    #         data_str += task.to_string()
            
    #         # omit newline on last write
    #         if i < len( self.active_tasks ) - 1 :
    #             data_str += '\n'

    #     # print( data_str ) 
                
    #     with open( CURRENT_TASKS_FILE, 'w' ) as f :
    #         f.write( data_str )



    
    # # todo needs mutex
    # def get_task_from_name( self, task_name ) :
    #     idx = self.get_task_index_from_name( task_name )
    #     return self.active_tasks[ idx ] 
    
    # # todo needs mutex
    # def get_task_index_from_name( self, task_name ) :
    #     tmp = [ task.name for task in self.active_tasks ] 
    #     return tmp.index( task_name ) 
    
        
    def change_task_name( self, previous_name, new_name ) :
        ... 

        
    def clear_progress( self, timescale ) :
        for task_name in self.current_progress_file :
            self.current_progress_file[ task_name ][ 'usage' ][ timescale ] = 0

            

    
            

    # def cron_save_active_tasks( self ) :

    #     while 1 :

    #         time.sleep( 20 )

    #         print( 'task_manager.py: needs save = ' + str( self.needs_save ) )

    #         if self.needs_save :

    #             self.needs_save = 0
    #             self.save_active_tasks()
