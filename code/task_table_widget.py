from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt


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
}
"""

class MyProgressBar( QProgressBar ):

    
    def __init__( self, parent = None ):
        QProgressBar.__init__(self, parent)
        self.setStyleSheet(DEFAULT_STYLE)
        self.completed = 0

        
    def setValue( self, value ):
        QProgressBar.setValue(self, value)

        if value == self.maximum():
            self.setStyleSheet(COMPLETED_STYLE)
            self.completed = 1

        else :
            if self.completed :
                self.setStyleSheet( DEFAULT_STYLE )
                self.completed = 0 





# class DraggbaleTableWidget( QTableWidget ) :

    

                



                

class TaskTableWidget( QWidget ) :
# class TaskTableManager( QWidget ) :


    # active_row = None
    active_timescale = 0
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

        timescale_labels = [ 'Day', 'Week', 'Month', 'Quarter', 'Year' ]

        self.timescale_combobox = QComboBox()
        self.timescale_combobox.addItems( timescale_labels )
        self.timescale_combobox.setCurrentIndex( self.active_timescale )
        self.timescale_combobox.activated.connect( self.timescale_combobox_activated )

        hlayout.addWidget( self.timescale_combobox ) 

        layout.addLayout( hlayout ) 

        nrows = len( self.task_manager ) 
        ncols = 3 # 4

        # self.table = TableWidgetDragRows( nrows, ncols ) 
        self.table = QTableWidget( nrows, ncols )

        self.table.setDragEnabled(True)
        self.table.setAcceptDrops(True)
        self.table.viewport().setAcceptDrops(True)
        self.table.setDragDropOverwriteMode(False)
        self.table.setDropIndicatorShown(True)
        self.table.setSelectionMode( QAbstractItemView.SingleSelection )
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setDragDropMode(QAbstractItemView.InternalMove)

        # hack
        self.table.dropEvent = self.dropEvent 
        
        # self.table.cellDoubleClicked.connect( self.cell_double_clicked ) 
        self.table.cellClicked.connect( self.cell_double_clicked )
        # self.table.cellRightClicked.connect( self.cell_right_clicked ) 
        
        self.table.setHorizontalHeaderLabels( [ 'Task', 'Budgeted', 'Spent',
                                                'Progress' ] )
        
        # self.table.horizontalHeader().setSectionResizeMode( QHeaderView.Stretch ) 
        # self.table.verticalHeader().setSectionResizeMode( QHeaderView.Stretch )

        self.table.horizontalHeader().setStretchLastSection( 1 )

        self.table.setSelectionBehavior( QAbstractItemView.SelectRows )
        self.table.setSelectionMode( QAbstractItemView.SingleSelection )
        self.table.verticalHeader().setSectionsMovable( 1 );

        self.table.setColumnWidth( 0, 200 )
        self.table.setColumnWidth( 1, 80 )
        # self.table.setColumnWidth( 2, 0 ) 

        for task_name in self.task_manager.get_task_names() :
            self.add_task_to_table( task_name, append = 0 ) 
        
        # for r in range( nrows ) :

        # self.reload() 
            
        layout.addWidget( self.table ) 
            
        hlayout = QHBoxLayout()

        add_button = QPushButton( '+' )
        delete_button = QPushButton( '-' )

        hlayout.addWidget( add_button ) 
        hlayout.addWidget( delete_button )

        add_button.clicked.connect( self.add_button_clicked )
        delete_button.clicked.connect( self.delete_button_clicked ) 

        layout.addLayout( hlayout ) 



    # note: for some reason, this correctly deletes the table that
    # was dragged originally. i'm not sure if it's actually deleted
    # behind the scenes, or if this is a QT memory leak. keeping for now
    # since it works and i can't see any performance issues if there is a leak.
    
    def dropEvent(self, event: QDropEvent):

        if not event.isAccepted() : # and event.source() == self:

            drop_row = self.drop_on( event ) 

            row = self.table.selectionModel().selectedRows()[0].row()
            task_name = self.table.cellWidget( row, 0 ).text() 

            print( row ) 
            print( drop_row ) 

            
            self.table.insertRow( drop_row )

            if row > drop_row :
                row += 1

            self.table.removeRow( row )

                        
            self.add_task_to_table( task_name, append = 0, row = drop_row ) 

            # event.accept()

            print( 'rowcount', self.table.rowCount() )

            
            self.sync_task_manager_rows() 
            self.sync_pomodoro_cbox_rows()

        
            # for row_index in range(len(rows_to_move)):
            #     self.cellWidget(drop_row + row_index, 0).setSelected(True)
            #     self.cellWidget(drop_row + row_index, 1).setSelected(True)
        # self.table.super().dropEvent(event)

        # print( self.cellWidget( drop_row, 0 ).text() ) 


    
    def drop_on(self, event):

        index = self.table.indexAt(event.pos())

        if not index.isValid():
            return self.table.rowCount()

        return index.row() + 1 if self.is_below(event.pos(), index) else index.row()

    
    def is_below(self, pos, index):
        rect = self.table.visualRect(index)
        margin = 2
        if pos.y() - rect.top() < margin:
            return False
        elif rect.bottom() - pos.y() < margin:
            return True
        # noinspection PyTypeChecker
        return rect.contains(pos, True) and not (int(self.table.model().flags(index))
                                                 & Qt.ItemIsDropEnabled) and pos.y() >= rect.center().y()




        
    def cell_double_clicked( self, row, col ) :

        if col != 0 :
             return 
         
        label = self.table.cellWidget( row, 0 )
        task_name = label.text()
        
        self.controller.pomodoro.set_task_cbox_task( task_name )

        # start timer if not running already 
        if not self.controller.pomodoro.running :
            self.controller.pomodoro.toggle_task_button_clicked() 



            
    def cell_right_clicked( self, row, col ) :

        if col != 0 :
             return 
         
        label = self.table.cellWidget( row, 0 )
        task_name = label.text()
        
        # self.controller.pomodoro.set_task_cbox_task( task_name )

        # # start timer if not running already 
        # if not self.controller.pomodoro.running :
        #     self.controller.pomodoro.toggle_task_button_clicked() 

        print( task_name ) 
        

            
        
    def timescale_combobox_activated( self ) :
         self.active_timescale = self.timescale_combobox.currentIndex()
         self.reload_table()
        
        

    # we obtain the task name directly from the label to account for the fact
    # that the user may change the task name. 
    def budget_entry_changed( self, task_name_label, new_budget ) :
        try :
            budgeted = float( new_budget )
        except :
            budgeted = 0

        task_name = task_name_label.text()
        timescale  = self.active_timescale

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

            

    def add_task_to_table( self, task_name, append = 1, row = -1 ) :
        
        timescale = self.active_timescale
        
        allocation = self.task_manager.get_budgeted( task_name, timescale )
        usage = self.task_manager.get_usage( task_name, timescale )

        if row == -1 : 
            row = self.task_manager.get_row( task_name )

        print( task_name, row ) 
            
        # policy = self.task_manager.get_policy( task_name, timescale )

        # add row at bottom
        if append : 
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
              
        self.table.setCellWidget( row, 2, bar )

        self.update_progress_bar( task_name ) 
        
        # bar = self.table.item( r, 2 )
        # print( bar )
        # print( type( bar ) ) 
        # bar.setFlags( bar.flags() ^ Qt.ItemIsEnabled )
        
        # self.table.


    def change_row_position( self, old_row, new_row ) :
        ... 
        

    # todo: move to inactive tasks 
    def delete_button_clicked( self ) :
        # task_name = self.get_active_task_name()
        # self.task_manager.delete_task( task_name ) 

        try : 
            active_row = self.table.selectionModel().selectedRows()[0].row()
        except :
            return 

        task_name = self.table.cellWidget( active_row, 0 ).text() 

        buttonReply = QMessageBox.question( self, 'Warning',
                                            'Delete task \"%s\"?' % task_name,
                                           QMessageBox.Yes | QMessageBox.No,
                                           QMessageBox.No)

        if buttonReply != QMessageBox.Yes:
            return
        
        self.table.removeRow( active_row ) 
            
        self.task_manager.delete_task( task_name )

        # get new active task 
        try : 
            active_row = self.table.selectionModel().selectedRows()[0].row()
            task_name = self.table.cellWidget( active_row, 0 ).text() 
            self.controller.pomodoro.active_task = task_name
        except :
            self.controller.pomodoro.active_task = ''
            return 
                
        task_name = self.table.cellWidget( active_row, 0 ).text() 
        
        self.sync_task_manager_rows() 
        self.sync_pomodoro_cbox_rows() 
        
        
        # active_row = 
        
        # self.delete_row( 
        

    def get_task_names( self ) :
        return [ self.table.cellWidget( row, 0 ).text()
                 for row in range(  self.table.rowCount() ) ]
        
        
    def set_active_row( self, task_name ) :
        ... 


    # set the rows of the task_manager to all current rows in the table
    def sync_task_manager_rows( self ) :
        for row in range( self.table.rowCount() ) :
            task_name = self.table.cellWidget( row, 0 ).text() 
            print( 'syncing rows: ', row, task_name ) 
            self.task_manager.set_row( task_name, row ) 

        

    def sync_pomodoro_cbox_rows( self ) :        
        self.controller.pomodoro.update_task_cbox() 
            

    def update_active_progress_bar( self ) :
        task_name = self.controller.pomodoro.active_task_name
        self.update_progress_bar( task_name ) 
        

    def load_table_row( self, task_name ) :
        timescale = self.active_timescale        
        usage = self.task_manager.get_usage( task_name, timescale )
        budgeted = self.task_manager.get_budgeted( task_name, timescale )
        row = self.task_manager.get_row( task_name )

        budgeted_entry = self.table.cellWidget( row, 1 )
        budgeted_entry.setText( str( '%.1f' % budgeted ) )
        
        self.update_progress_bar( task_name ) 

        
        
    def update_progress_bar( self, task_name ) :
        # task = self.task_manager.active_tasks[ row ]

        timescale = self.active_timescale
        
        usage = self.task_manager.get_usage( task_name, timescale )
        allocation = self.task_manager.get_budgeted( task_name, timescale )
        row = self.task_manager.get_row( task_name )
        
        if allocation == 0 : 
            progress = 0 
        else :
            progress = TASK_BAR_MAX * usage / allocation

        progress = min( progress, TASK_BAR_MAX )
        
        bar = self.table.cellWidget( row, 2 )
        bar.setValue( progress )

        hours, mins = divmod( usage * 60, 60 )
        label = '%d:%s' % ( int( hours ), str( int( mins ) ).zfill(2) )

        bar.setToolTip( label )


    # def update_usage( self, row ) :
    #     task = self.task_manager.active_tasks[ row ]
    #     usage_label = self.table.cellWidget( row, 2 )
    #     usage_label.setText( '%.2f' % task.usage )


    # reload all data from task manager 
    def reload_table( self ) :

        for task_name in self.task_manager.get_task_names() :
            # self.update_usage( r )
            self.load_table_row( task_name )
            # self.update_progress_bar( task_name ) 
        




            
# class EnterTaskNameDialog( QDialog ) :

#     def __init__( self, task_table_widget ) :
#         super().__init__() 
#         self.task_table_widget = task_table_widget

        
