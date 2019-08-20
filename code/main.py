from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5 import QtCore

import atexit 


import gui_config


# custom managers
from task_manager import TaskManager
from time_transaction_manager import TimeTransactionManager
from time_manager import TimeManager 


# custom widgets 
from toolbar_widget import ToolbarWidget 
from pomodoro_widget import PomodoroWidget
from task_table_widget import TaskTableWidget
from schedule_widget import ScheduleWidget 
from task_options_widget import TaskOptionsWidget
from time_transaction_widget import TimeTransactionWidget

# from goal_widget import GoalWidget 

import signal
import sys 






# register control-c as program quit 
signal.signal(signal.SIGINT, signal.SIG_DFL)


class Controller( object ) :
    
    # task_manager = None
    # time_manager = None
    
    # task_table = None
    # time_manager = None
    # task_options = None 
    
        
    def __init__( self ) :
        pass 
    
    def init( self, task_manager, time_manager, time_transaction_manager,
              task_table, pomodoro, task_options, time_transaction_widget  ) :
        
        self.task_manager = task_manager
        self.time_manager = time_manager 
        self.time_transaction_manager = time_transaction_manager

        self.task_table = task_table
        self.pomodoro = pomodoro
        self.task_options = task_options 
        self.time_transaction_widget = time_transaction_widget


    
class App( QWidget ) :

    def __init__(self ):
        super().__init__()

        self.setWindowTitle( 'YNAB-T' )
        self.resize( gui_config.WINDOW_WIDTH, gui_config.WINDOW_HEIGHT )
        
        layout = QVBoxLayout()
        self.setLayout( layout ) 

        controller = Controller() 
        
        # all managers 
        task_manager = TaskManager( controller ) 
        time_manager = TimeManager( controller )
        time_transaction_manager = TimeTransactionManager( controller )

        atexit.register( task_manager.close ) 
        
        # all widgets 
        task_table = TaskTableWidget( controller )
        pomodoro = PomodoroWidget( controller )
        
        # schedule = ScheduleWidget( task_manager )
        task_options = TaskOptionsWidget( controller ) 
        time_transaction_widget = TimeTransactionWidget( controller )


        controller.init( task_manager, time_manager, time_transaction_manager,
                         task_table, pomodoro, task_options,
                          time_transaction_widget ) 

        task_manager.init()
        time_manager.init()
        time_transaction_manager.init()

        task_table.init()
        pomodoro.init()
        task_options.init()
        time_transaction_widget.init()
        
        vlayout = QVBoxLayout()
        vlayout.addWidget( pomodoro )
        vlayout.addWidget( task_options ) 
        vlayout.addWidget( time_transaction_widget ) 

        hlayout = QHBoxLayout()
        hlayout.addWidget( task_table )
        hlayout.addLayout( vlayout ) 
        
        layout.addLayout( hlayout ) 
        
        # toolbar = ToolbarWidget( pomodoro )
        # layout.addWidget( toolbar )

        

    def closeEvent( self, event ) :
        sys.exit(0)
        
                
    
    
# enter program 
if __name__ == '__main__':  
    app = QApplication(sys.argv)
    # app.setStyleSheet( 'QGroupBox { font-weight: bold; border-radius: 5px; border: 2px solid black }' )
    app.setStyleSheet( 'QGroupBox { font-weight: bold; }' )
    # app.setStyleSheet( 'QProgressBar { background-color: green; }' ) 
    ex = App()
    ex.show()
    sys.exit( app.exec_() )
    



