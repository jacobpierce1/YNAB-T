from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QFont, QPixmap
from PyQt5 import QtCore





class PomodoroWidget( QWidget ) :

    direction = -1  # -1 for decrease (pomodoro mode), 1 for increase (stopwatch)

    hours = 0
    mins = 0
    secs = 0

    label = None  # store the QWidget 
    
    
    def __init__( self ) :
        super().__init__()

        toplayout = QHBoxLayout()
        self.setLayout( toplayout )

        box = QGroupBox( 'Pomodoro' )
        layout = QVBoxLayout()
        box.setLayout( layout ) 
        toplayout.addWidget( box ) 
        
        self.label = QLabel( '00:00:00' )
        font = self.label.font()
        font.setPointSize( 72 )
        font.setBold( 1 )
        self.label.setFont( font ) 
        layout.addWidget( self.label ) 

        



    def pause( self ) :
        ...


    def start( self ) :
        ... 
        

    def reset( self ) :
        ... 
