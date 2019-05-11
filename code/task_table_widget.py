from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore






class TaskTableWidget( QWidget ) :

    def __init__( self ) :
        super().__init__()
        
        toplayout = QHBoxLayout()
        self.setLayout( toplayout )

        box = QGroupBox( 'Task Table' )
        layout = QVBoxLayout()
        box.setLayout( layout ) 
        toplayout.addWidget( box )

        nrows = 10
        ncols = 2
        
        self.table = QTableWidget( nrows, ncols ) 

        self.table.setHorizontalHeaderLabels( [ 'Category', 'Budgeted', 'Spent',
                                                'Progress' ] )
        
        self.table.horizontalHeader().setSectionResizeMode( QHeaderView.Stretch ) 
        self.table.verticalHeader().setSectionResizeMode( QHeaderView.Stretch )
        
        for r in range( nrows ) :
            bar = QProgressBar()
            bar.setMaximum( 1000 )
            bar.setMinimum( 0 )
            bar.setValue( 500 ) 
            bar.setOrientation( QtCore.Qt.Horizontal )
            self.table.setCellWidget( r, 1, bar ) 
        
        
        layout.addWidget( self.table ) 
