from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore

import time 
import threading 


USE_SECONDS = 0


class PomodoroWidget( QWidget ) :

    direction = 1  # -1 for decrease (pomodoro mode), 1 for increase (stopwatch)

    hours = 0
    mins = 0
    secs = 0

    label = None  # store the QWidget
    elapsed = 0
    running = 0

    
    # timer start and previous time 
    start_time = 0  # time since toggle last clicked to start timer
    previous_time = 0   # current value on timer in seconds 

    # task metadata and task timing data
    # task_start_time = 0
    task_previous_time = 0
    # task = None 
    # progress_bar = None
    # row = 0  # row in the table corresponding to this task

    active_task_name = None 
    
    timer_updated_signal = QtCore.pyqtSignal()

    
    def __init__( self, controller ) :
        super().__init__()
        self.controller = controller


    def init( self ) :

        self.task_manager = self.controller.task_manager
        self.task_table = self.controller.task_table 

        self.start_time = time.time() 
        
        toplayout = QHBoxLayout()
        self.setLayout( toplayout )

        box = QGroupBox( 'Pomodoro' )
        layout = QVBoxLayout()
        box.setLayout( layout ) 
        toplayout.addWidget( box ) 
        
        self.label = QLabel( '00:00' )
        font = self.label.font()
        font.setPointSize( 100 )
        font.setBold( 1 )
        self.label.setFont( font ) 
        layout.addWidget( self.label ) 

        hlayout = QVBoxLayout()

        # add_button = QPushButton( '+ 1 min' )
        # delete_button = QPushButton( '- 1 min' )

        # hlayout.addWidget( add_button ) 
        # hlayout.addWidget( delete_button ) 


        self.task_cbox = QComboBox()
        hlayout.addWidget( self.task_cbox )
        self.task_cbox.activated.connect( self.task_cbox_activated ) # when used selects
        self.update_task_cbox()
        self.task_cbox_activated()
        

        self.mode_cbox = QComboBox()
        self.mode_cbox.addItems( [ 'Ascend', 'Descend' ] )
        hlayout.addWidget( self.mode_cbox )
                 
        self.toggle_task_button = QPushButton( 'Start Task' )
        self.toggle_task_button.clicked.connect( self.toggle_task_button_clicked ) 
        hlayout.addWidget( self.toggle_task_button )

        # set to "running", but immediately reset.
        self.running = 1 
        self.toggle_task_button_clicked() 

        
        reset_button = QPushButton( 'Reset Task' ) 
        reset_button.clicked.connect( self.reset_button_clicked )
        hlayout.addWidget( reset_button )

        # full_screen_button = QPushButton( 'Full Screen' ) 
        # full_screen_button.clicked.connect( self.full_screen_button_clicked )
        # hlayout.addWidget( full_screen_button ) 

        layout.addLayout( hlayout )


        # system tray
        # text = QLabel( 'testing testing' ) 
        icon = QIcon( 'icon.png' ) 
        self.tray = QSystemTrayIcon()
        self.tray.setIcon( icon )
        self.tray.setVisible(True)



        self.timer_updated_signal.connect( self.task_table.update_active_progress_bar )
        self.timer_updated_signal.connect( self.update_timer_label )
        
        timer_update_thread = threading.Thread( target = self.update_timer_target,
                                                daemon = 1 )
        timer_update_thread.start() 


        
        # self.pomodoro_thread = PomodoroThread( self, task_manager, task_table ) 
        # self.pomodoro_thread.start() 


    def update_task_cbox( self ) :
        self.task_cbox.clear()

        tasks = self.task_manager.get_task_names()
        self.task_cbox.addItems( tasks )

        task_name = self.task_cbox.currentText()
        self.active_task_name = task_name


        
    def task_cbox_activated( self ) :

        task_name = self.task_cbox.currentText()
        # self.task = self.task_manager.get_task_from_name( task_name ) 
        # self.task_table.active_row = self.task_manager.get_task_index_from_name( task_name )
        # self.progress_bar = self.task_table.cellWidget

        self.active_task_name = task_name

        if self.active_task_name : 
            self.reset_button_clicked() 
        
        

    def toggle_task_button_clicked( self ) :

        self.running = not self.running
            
        if self.running :
            self.start_time = time.time()
            self.toggle_task_button.setText( 'Working' )
            self.toggle_task_button.setStyleSheet("background-color: #D9EB45")

        else :
            self.previous_time += time.time() - self.start_time
            self.toggle_task_button.setText( 'Paused' ) 
            self.toggle_task_button.setStyleSheet("background-color: #E55959")
            

                
    def reset_button_clicked( self ) :
        self.start_time = time.time()
        self.previous_time = 0
        timescale =  self.task_table.current_timescale 

        print( self.active_task_name ) 
        
        self.task_previous_time = self.task_manager.get_usage( self.active_task_name,
                                                               timescale ) 

        
    # def full_screen_button_clicked( self ) :
    #     ...


    # def pause( self ) :
    #     ...


    # def start( self ) :
    #     ... 
        
    # def reset( self ) :
    #     ... 

    def update_timer_label( self ) :
        
        hours, mins = divmod( self.elapsed, 60 ) 
        
        label = '%d:%s' % ( int( hours ), str( int( mins ) ).zfill(2) )
        self.label.setText( label ) 

        # icon = QIcon( self.label.pixmap() )
        icon = QIcon( 'icon.png' )
        
        # # todo 
        # self.tray.setIcon( icon )
        # self.tray.setVisible(True)
        # self.tray.show() 
        

    def update_timer_target( self ) :

        # time.sleep( 5 ) 
        
        while 1 :

            if self.running :
            
                # compute timer time in seconds 
                elapsed = time.time() - self.start_time + self.previous_time

                # convert elapsed to minutes. to debug and use seconds, comment this out
                if not USE_SECONDS : 
                    elapsed /= 60
                    
                self.elapsed = elapsed 

                # track task time in hours
                task_name = self.active_task_name 
                new_usage = self.task_previous_time + elapsed / 60
                timescale = self.controller.task_table.current_timescale
                self.controller.task_manager.set_usage( task_name, new_usage, timescale )
                                                        
                                                        
                # self.task_manager.needs_save = 1

                self.timer_updated_signal.emit() 

                if USE_SECONDS : 
                    time.sleep( 0.2 )

                else :
                    time.sleep( 5 ) 
