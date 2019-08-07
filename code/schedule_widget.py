from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore


from schedule_db import ScheduleDB 


class ScheduleWidget( QWidget ) :

    def __init__( self, task_manager ) :
        super().__init__()

        self.task_manager = task_manager 
        
        toplayout = QHBoxLayout()
        self.setLayout( toplayout )

        box = QGroupBox( 'Schedule' )
        layout = QVBoxLayout()
        box.setLayout( layout ) 
        toplayout.addWidget( box )

        ncols = 4
        nrows = 5

        self.table = QTableWidget( nrows, ncols ) 
        
        self.table.setHorizontalHeaderLabels( [ 'Task', 'Start', 'End', 'Elapsed' ] )
        
        self.table.horizontalHeader().setSectionResizeMode( QHeaderView.Stretch ) 
        self.table.verticalHeader().setSectionResizeMode( QHeaderView.Stretch )
        
        layout.addWidget( self.table )
        
        for r in range( nrows ) :
            cbox = QComboBox()
            cbox.addItems( self.task_manager.active_tasks ) 
                    
            self.table.setCellWidget( r, 0, cbox )
            self.table.setCellWidget( r, 1, QLineEdit() )
            self.table.setCellWidget( r, 2, QLineEdit() )

        
        hlayout = QHBoxLayout()

        add_button = QPushButton( '+' )
        delete_button = QPushButton( '-' )

        hlayout.addWidget( add_button ) 
        hlayout.addWidget( delete_button ) 

        layout.addLayout( hlayout ) 
        
