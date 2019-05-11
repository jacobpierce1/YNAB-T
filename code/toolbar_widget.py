from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QFont, QPixmap
from PyQt5 import QtCore





class ToolbarWidget( QWidget ) :
    
    def __init__( self, pomodoro ) :
        super().__init__()

        self.pomodoro = pomodoro

        toplayout = QHBoxLayout()
        self.setLayout( toplayout )

        box = QGroupBox( 'Toolbar' )
        layout = QHBoxLayout()
        box.setLayout( layout ) 
        toplayout.addWidget( box ) 

        toggle_task_button = QPushButton( 'Toggle Task' )
        toggle_task_button.clicked.connect( self.toggle_task_button_clicked ) 
        layout.addWidget( toggle_task_button )
        
        # pause_task_button = QPushButton( 'Pause Task' )
        # start_task_button.clicked.connect( self.pause_task_button_clicked )
        # layout.addWidget( pause_task_button )
        
        reset_task_button = QPushButton( 'Reset Task' ) 
        reset_task_button.clicked.connect( self.reset_task_button_clicked )
        layout.addWidget( reset_task_button )

        full_screen_button = QPushButton( 'Full Screen' ) 
        full_screen_button.clicked.connect( self.full_screen_button_clicked )
        layout.addWidget( full_screen_button ) 

        


    def toggle_task_button_clicked( self ) :
        ...

                
    def reset_task_button_clicked( self ) :
        ...

        
    def full_screen_button_clicked( self ) :
        ...
