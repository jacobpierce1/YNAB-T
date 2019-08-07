from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5 import QtCore

import atexit 


import gui_config


# custom managers
from task_manager import TaskManager

# custom widgets 
from toolbar_widget import ToolbarWidget 
from pomodoro_widget import PomodoroWidget
from task_table_widget import TaskTableWidget
from schedule_widget import ScheduleWidget 
from task_options_widget import TaskOptionsWidget
from time_manager import TimeManager 
# from goal_widget import GoalWidget 


import signal
import sys 

# register control-c as program quit 
signal.signal(signal.SIGINT, signal.SIG_DFL)




    
class App( QWidget ) :

    def __init__(self ):
        super().__init__()

        self.setWindowTitle( 'YNAB-T' )
        self.resize( gui_config.WINDOW_WIDTH, gui_config.WINDOW_HEIGHT )
        
        layout = QVBoxLayout()
        self.setLayout( layout ) 

        # all managers 
        task_manager = TaskManager() 

        atexit.register( task_manager.save_active_tasks ) 
        
        # all widgets 
        task_table = TaskTableWidget( task_manager )
        pomodoro = PomodoroWidget( task_manager, task_table )
        time_manager = TimeManager( task_manager, task_table ) 
        # schedule = ScheduleWidget( task_manager )
        task_options = TaskOptionsWidget() 

        vlayout = QVBoxLayout()
        vlayout.addWidget( pomodoro )
        # vlayout.addWidget( schedule )
        vlayout.addWidget( task_options ) 
        
        hlayout = QHBoxLayout()
        hlayout.addWidget( task_table )
        hlayout.addLayout( vlayout ) 
        
        layout.addLayout( hlayout ) 
        
        toolbar = ToolbarWidget( pomodoro )
        layout.addWidget( toolbar )

        

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
    



