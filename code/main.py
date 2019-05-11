from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5 import QtCore


import gui_config 
from toolbar_widget import ToolbarWidget 
from pomodoro_widget import PomodoroWidget
from task_table_widget import TaskTableWidget
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

        
        pomodoro = PomodoroWidget()
        task_table = TaskTableWidget()

        tmplayout = QHBoxLayout()
        tmplayout.addWidget( task_table )
        tmplayout.addWidget( pomodoro ) 
        layout.addLayout( tmplayout ) 
        
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
    



