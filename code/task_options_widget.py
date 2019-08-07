from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore


# from task_options_manager import TaskOptionsManager 


TASK_OPTIONS_EXCESS_POLICIES = [ 'Good', 'Bad', 'Neutral' ]


class TaskOptionsWidget( QWidget ) :


    def __init__( self ) :
        super().__init__()

        toplayout = QHBoxLayout()
        self.setLayout( toplayout )

        box = QGroupBox( 'Task Options' )
        layout = QFormLayout()
        box.setLayout( layout ) 
        toplayout.addWidget( box )
        
        self.excess_policy_cbox = QComboBox()
        self.excess_policy_cbox.addItems( TASK_OPTIONS_EXCESS_POLICIES ) 

        layout.addRow( 'Excess Policy', self.excess_policy_cbox )

        button = QPushButton( 'Budget X to meet weekly goal' )
        
        layout.addRow( button ) 
