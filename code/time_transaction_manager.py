import gui_config 
import sqlite3 

TASKS_DATABASE = gui_config.data_path + 'task_db.sqlite3'



class TimeTransactionDB( object ) : 

	... 
	


class TimeTransactionManager( object ) :

	def __init__( self, controller ) :

		self.controller = controller 
        
        # self.tasks_database = 
	def init( self ) : 
		...	

	def compute_progress_for_timescale( self, timescale, date ) : 
		... 

	def rename_entries( self, old_name, new_name ) : 
		... 


	def sync_current_progress_file( self ) : 
		... 

	# get N most recent transactions 
	def get_recent_transactions( self, N ) : 
		...
