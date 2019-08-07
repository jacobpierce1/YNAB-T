import os 
import gui_config
import threading
import time


data_path = os.path.dirname(os.path.abspath(__file__)) + '/../'
    
if gui_config.DEVELOPER_MODE :
    data_path += '.local_debug/'
else :
    data_path += '.local/'

CURRENT_TASKS_FILE = data_path + 'active_tasks.txt'


EXCESS_GOOD, EXCESS_BAD, EXCESS_NEUTRAL = [ 0, 1, 2 ] 



class Task( object ) :
    
    def __init__( self, task_name, allocation = 0,
                  usage = 0, policy = EXCESS_NEUTRAL ) :

        self.name = task_name
        self.allocation = allocation
        self.usage = usage
        self.policy = policy
        

    def to_string( self ) :
        return '%s\t%.1f\t%.2f\t%d' % ( self.name, self.allocation,
                                        self.usage, self.policy )
        
    
    @classmethod
    def from_string( cls, s ) :
        tmp = [ t(x) for t,x in zip( [ str, float, float, int ],
                                     s.split( '\t' ) ) ] 
        task_name, allocation, usage, policy = tmp
        return cls( task_name, allocation, usage, policy ) 




    
    
class TaskManager( object ) :

    active_tasks = None
    needs_save = 0
    
    def __init__( self ) :
        self.load_active_tasks()

        cron = threading.Thread( target = self.cron_save_active_tasks,
                                                          daemon = 1 )
        cron.start() 
        

    def load_active_tasks( self ) :

        self.active_tasks = []
        
        with open( CURRENT_TASKS_FILE, 'r' ) as f :
            for line in f.readlines() :
                self.active_tasks.append( Task.from_string( line ) )
                
                
                
    def save_active_tasks( self ) :

        print( 'task_manager.py: saving active tasks' ) 

        data_str = ''

        for i in range( len( self.active_tasks ) ) :
            task = self.active_tasks[i] 
            data_str += task.to_string()
            
            # omit newline on last write
            if i < len( self.active_tasks ) - 1 :
                data_str += '\n'

        # print( data_str ) 
                
        with open( CURRENT_TASKS_FILE, 'w' ) as f :
            f.write( data_str )


    # todo needs mutex
    def get_task_from_name( self, task_name ) :
        idx = self.get_task_index_from_name( task_name )
        return self.active_tasks[ idx ] 
    
    # todo needs mutex
    def get_task_index_from_name( self, task_name ) :
        tmp = [ task.name for task in self.active_tasks ] 
        return tmp.index( task_name ) 
    
        
    def add_task( self ) :
        ...


    def delete_task( self ) :
        ... 

    def change_task_name( self ) :
        ... 

        
    def clear_progress( self ) :

        for task in self.active_tasks :
            task.usage = 0

        self.save_active_tasks()
            

    def __len__( self ) :
        return len( self.active_tasks ) 
        

    def cron_save_active_tasks( self ) :

        while 1 :

            time.sleep( 20 )

            print( 'task_manager.py: needs save = ' + str( self.needs_save ) )

            if self.needs_save :

                self.needs_save = 0
                self.save_active_tasks()
