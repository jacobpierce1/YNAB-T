from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore


from task_manager import TaskManager 


# bar resolution 
TASK_BAR_MAX = 1000 





DEFAULT_STYLE = """
QProgressBar{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center
}

QProgressBar::chunk {
    background-color: lightblue;
    width: 10px;
    margin: 1px;
}
"""

COMPLETED_STYLE = """
QProgressBar{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center
}

QProgressBar::chunk {
    background-color: red;
    width: 10px;
    margin: 1px;
}
"""

class MyProgressBar( QProgressBar ):
    def __init__(self, parent = None):
        QProgressBar.__init__(self, parent)
        self.setStyleSheet(DEFAULT_STYLE)

    def setValue(self, value):
        QProgressBar.setValue(self, value)

        if value == self.maximum():
            self.setStyleSheet(COMPLETED_STYLE)







class TaskTableWidget( QWidget ) :


    active_row = None
    
    def __init__( self, task_manager ) :
        super().__init__()

        self.task_manager = task_manager 
        
        toplayout = QHBoxLayout()
        self.setLayout( toplayout )

        box = QGroupBox( 'Task Table' )
        layout = QVBoxLayout()
        box.setLayout( layout ) 
        toplayout.addWidget( box )


        hlayout = QHBoxLayout()
        daily_button = QPushButton( 'Daily' )
        daily_button.clicked.connect( self.daily_button_clicked ) 
        hlayout.addWidget( daily_button )

        weekly_button = QPushButton( 'Weekly' )
        weekly_button.clicked.connect( self.weekly_button_clicked ) 
        hlayout.addWidget( weekly_button )

        monthly_button = QPushButton( 'Monthly' )
        monthly_button.clicked.connect( self.monthly_button_clicked ) 
        hlayout.addWidget( monthly_button ) 

        layout.addLayout( hlayout ) 

        nrows = len( self.task_manager ) 
        ncols = 3 # 4
        
        self.table = QTableWidget( nrows, ncols ) 

        self.table.setHorizontalHeaderLabels( [ 'Task', 'Budgeted', 'Spent',
                                                'Progress' ] )
        
        # self.table.horizontalHeader().setSectionResizeMode( QHeaderView.Stretch ) 
        # self.table.verticalHeader().setSectionResizeMode( QHeaderView.Stretch )

        self.table.horizontalHeader().setStretchLastSection( 1 );

        
        self.table.setColumnWidth( 0, 200 )
        self.table.setColumnWidth( 1, 80 )
        # self.table.setColumnWidth( 2, 0 ) 
        
        for r in range( nrows ) :

            task = self.task_manager.active_tasks[ r ]
            
            self.table.setCellWidget( r, 0, QLabel( task.name ) )
            self.table.setCellWidget( r, 1, QLineEdit( '%.1f' % task.allocation ) )
            # self.table.setCellWidget( r, 2, QLabel( '%.2f' % task.usage ) )

            bar = MyProgressBar()
            bar.setMaximum( TASK_BAR_MAX )
            bar.setMinimum( 0 )
            progress = TASK_BAR_MAX * task.usage / task.allocation
            bar.setValue( progress ) 
            bar.setOrientation( QtCore.Qt.Horizontal )
            self.table.setCellWidget( r, 2, bar ) 


        self.reload() 
            
        layout.addWidget( self.table ) 
            
        hlayout = QHBoxLayout()

        add_button = QPushButton( '+' )
        delete_button = QPushButton( '-' )

        hlayout.addWidget( add_button ) 
        hlayout.addWidget( delete_button ) 

        layout.addLayout( hlayout ) 

        


    def daily_button_clicked( self ) :
        ...

        
    def weekly_button_clicked( self ) :
        ...

        
    def monthly_button_clicked( self ) :
        ...

        
    def set_active_row( self, task_name ) :
        ... 
        

    def update_active_progress_bar( self ) :
        self.update_progress_bar( self.active_row ) 
        

    def update_progress_bar( self, row ) :
        task = self.task_manager.active_tasks[ row ]

        progress = TASK_BAR_MAX * task.usage / task.allocation
        progress = min( progress, TASK_BAR_MAX )

        bar = self.table.cellWidget( row, 2 )
        bar.setValue( progress )

        # if progress == TASK_BAR_MAX :
            

        hours, mins = divmod( task.usage * 60, 60 )
        label = '%d:%s' % ( int( hours ), str( int( mins ) ).zfill(2) )

        bar.setToolTip( label )


    # def update_usage( self, row ) :
    #     task = self.task_manager.active_tasks[ row ]
    #     usage_label = self.table.cellWidget( row, 2 )
    #     usage_label.setText( '%.2f' % task.usage )


    # reload all data from task manager 
    def reload( self ) :

        for r in range( len( self.task_manager.active_tasks ) ) :
            # self.update_usage( r )             
            self.update_progress_bar( r ) 
        
