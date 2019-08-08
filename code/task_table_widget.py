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


    # active_row = None
    current_timescale = 1
    active_task_name = None 
    
    
    def __init__( self, controller ) :
        super().__init__()
        self.controller = controller


        
    def init( self ) :
        
        # self.controller = controller
        
        self.task_manager = self.controller.task_manager 
        
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

        # dynamically expand
        nrows = 0 # len( self.task_manager ) 
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

        for task_name in self.task_manager.get_task_names() :
            self.add_task_to_table( task_name ) 
        
        # for r in range( nrows ) :

        self.reload() 
            
        layout.addWidget( self.table ) 
            
        hlayout = QHBoxLayout()

        add_button = QPushButton( '+' )
        delete_button = QPushButton( '-' )

        hlayout.addWidget( add_button ) 
        hlayout.addWidget( delete_button )

        add_button.clicked.connect( self.add_button_clicked )
        delete_button.clicked.connect( self.delete_button_clicked ) 

        layout.addLayout( hlayout ) 



    # we obtain the task name directly from the label to account for the fact
    # that the user may change the task name. 
    def budget_entry_changed( self, task_name_label, new_budget ) :
        try :
            budgeted = float( new_budget )
        except :
            budgeted = 0

        task_name = task_name_label.text()
        timescale  = self.current_timescale

        self.task_manager.current_progress_file[ task_name ][ 'budgeted' ][ timescale ] = budgeted 
        self.update_progress_bar( task_name ) 
                    
        

    def add_button_clicked( self ) :

        task_name, okPressed = QInputDialog.getText( self, 'Enter Task Name', '',
                                                QLineEdit.Normal, '' )
        
        if okPressed and task_name != '':
            self.task_manager.add_task( task_name )
            self.add_task_to_table( task_name ) 
            self.controller.pomodoro.update_task_cbox()

        else :
            print( 'ERORR: unable to add task...' )

            

    def add_task_to_table( self, task_name ) :
        
        timescale = self.current_timescale
        
        allocation = self.task_manager.get_budgeted( task_name, timescale )
        usage = self.task_manager.get_usage( task_name, timescale )
        row = self.task_manager.get_row( task_name )
        # policy = self.task_manager.get_policy( task_name, timescale )


        print( 'adding task to task table' )
        print( allocation )
        print( usage )
        print( row ) 

        # add row at bottom 
        self.table.insertRow( self.table.rowCount() )

        task_name_label = QLabel( task_name )
        self.table.setCellWidget( row, 0, task_name_label )

        allocation_entry = QLineEdit( '%.1f' % allocation )
        allocation_entry.setValidator( QDoubleValidator() )

        tmp = lambda event : self.budget_entry_changed( task_name_label, event )
        allocation_entry.textChanged[ str ].connect( tmp )
        
        self.table.setCellWidget( row, 1, allocation_entry ) 
        # self.table.setCellWidget( r, 2, QLabel( '%.2f' % task.usage ) )
        
        bar = MyProgressBar()
        bar.setMaximum( TASK_BAR_MAX )
        bar.setMinimum( 0 )

        if allocation == 0 : 
            progress = 0
        else : 
            progress = TASK_BAR_MAX * usage / allocation
            
        bar.setValue( progress ) 
        bar.setOrientation( QtCore.Qt.Horizontal )
        
        self.table.setCellWidget( row, 2, bar )
        
        # bar = self.table.item( r, 2 )
        # print( bar )
        # print( type( bar ) ) 
        # bar.setFlags( bar.flags() ^ Qt.ItemIsEnabled )
        
        # self.table.



    # todo: move to inactive tasks 
    def delete_button_clicked( self ) :
        # task_name = self.get_active_task_name()
        # self.task_manager.delete_task( task_name ) 
        ...
        

    def daily_button_clicked( self ) :
        ...

        
    def weekly_button_clicked( self ) :
        ...

        
    def monthly_button_clicked( self ) :
        ...

        
    def set_active_row( self, task_name ) :
        ... 
        

    def update_active_progress_bar( self ) :
        task_name = self.controller.pomodoro.active_task_name
        self.update_progress_bar( task_name ) 
        

    def update_progress_bar( self, task_name ) :
        # task = self.task_manager.active_tasks[ row ]

        timescale = self.current_timescale
        
        usage = self.task_manager.get_usage( task_name, timescale )
        allocation = self.task_manager.get_budgeted( task_name, timescale )
        row = self.task_manager.get_row( task_name )

        print( 'update progress bar' ) 
        print( allocation )
        print( usage )
        print( row ) 
        
        if allocation == 0 : 
            progress = 0 
        else :
            progress = TASK_BAR_MAX * usage / allocation

        progress = min( progress, TASK_BAR_MAX )
        
        bar = self.table.cellWidget( row, 2 )
        bar.setValue( progress )

        # if progress == TASK_BAR_MAX :
            

        hours, mins = divmod( usage * 60, 60 )
        label = '%d:%s' % ( int( hours ), str( int( mins ) ).zfill(2) )

        bar.setToolTip( label )


    # def update_usage( self, row ) :
    #     task = self.task_manager.active_tasks[ row ]
    #     usage_label = self.table.cellWidget( row, 2 )
    #     usage_label.setText( '%.2f' % task.usage )


    # reload all data from task manager 
    def reload( self ) :

        for task_name in self.task_manager.get_task_names() :
            # self.update_usage( r )             
            self.update_progress_bar( task_name ) 
        




            
# class EnterTaskNameDialog( QDialog ) :

#     def __init__( self, task_table_widget ) :
#         super().__init__() 
#         self.task_table_widget = task_table_widget

        
