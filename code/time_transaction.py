import gui_config


class TimeTransaction( object ) :

	def __init__( self, task_id = -1, task_name = None, 
				start_time = None, stop_time = None ) : 

		self.task_id = task_id
		self.task_name = task_name 
		self.start_time = start_time 
		self.stop_time = stop_time 

	
	def to_tuple( self ) : 
		return ( self.task_id, self.task_name, self.start_time, self.stop_time )
 

	def from_tuple( self ) : 
		...
		