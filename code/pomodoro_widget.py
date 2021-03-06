from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore

from PIL import Image, ImageDraw,ImageFont
import time 
import threading 
import numpy as np
import matplotlib.font_manager as fm
import sys

import gui_config


if gui_config.DEVELOPER_MODE :  
    USE_SECONDS = 1
else : 
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
    task_previous_times = None
    # task = None 
    # progress_bar = None
    # row = 0  # row in the table corresponding to this task

    active_task_name = None 
    
    timer_updated_signal = QtCore.pyqtSignal()

    lock = None

    
    def __init__( self, controller ) :
        super().__init__()
        self.controller = controller


    def init( self ) :

        self.task_manager = self.controller.task_manager
        self.task_table = self.controller.task_table 

        self.task_previous_times = np.zeros( gui_config.NUM_TIMESCALES )
        
        self.start_time = time.time()
        self.lock = threading.Lock() 
        
        toplayout = QHBoxLayout()
        self.setLayout( toplayout )

        box = QGroupBox( 'Pomodoro' )
        layout = QVBoxLayout()
        box.setLayout( layout ) 
        toplayout.addWidget( box ) 
        
        self.label = QLabel( '0:00' )
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
        self.task_cbox.currentIndexChanged.connect( self.task_cbox_activated ) # when used selects
        self.update_task_cbox()
        self.task_cbox_activated()
        

        self.mode_cbox = QComboBox()
        self.mode_cbox.addItems( [ 'Ascend', 'Descend' ] )
        hlayout.addWidget( self.mode_cbox )
                 
        self.toggle_task_button = QPushButton( 'Start Task' )
        self.toggle_task_button.clicked.connect( self.toggle_task_button_clicked ) 
        hlayout.addWidget( self.toggle_task_button )

        # system tray
        # text = QLabel( 'testing testing' ) 
        icon = QIcon( 'icon.png' ) 
        self.tray = QSystemTrayIcon()
        self.tray.setIcon( icon )
        self.tray.setVisible(True)
        self.tray.activated.connect( self.toggle_task_button_clicked )

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


        self.timer_updated_signal.connect( self.task_table.update_active_progress_bar )
        self.timer_updated_signal.connect( self.update_timer_label )
        
        timer_update_thread = threading.Thread( target = self.update_timer_target,
                                                daemon = 1 )
        timer_update_thread.start() 


        
        # self.pomodoro_thread = PomodoroThread( self, task_manager, task_table ) 
        # self.pomodoro_thread.start() 


    # set a particular task in the combo box
    # automatically triggers task_cbox_activated. 
    def set_task_cbox_task( self, task_name ) :

        # print( task_name )

        if not task_name :
            return

        index = self.task_cbox.findText( task_name );

        # print( index ) 
        
        if index != -1 :
            self.task_cbox.setCurrentIndex( index );

        else :
            print( 'ERROR (FATAL): attempted to set the pomodoro cbox task to a non-existent task.' )
            sys.exit( -1 ) 
        
        
        
        
    def update_task_cbox( self, set_default_active_task = 1 ) :
        self.task_cbox.clear()

        # tasks = self.task_manager.get_task_names()
        tasks = self.controller.task_table.get_task_names() 
        self.task_cbox.addItems( tasks )

        if set_default_active_task : 
            task_name = self.task_cbox.currentText()
            self.active_task_name = task_name

        else :
            self.set_task_cbox_task() 
            

        
    def task_cbox_activated( self ) :

        task_name = self.task_cbox.currentText()
        # self.task = self.task_manager.get_task_from_name( task_name ) 
        # self.task_table.active_row = self.task_manager.get_task_index_from_name( task_name )
        # self.progress_bar = self.task_table.cellWidget

        with self.lock : 
        
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
            self.update_timer_label() 

                
    def reset_button_clicked( self ) :
        self.start_time = time.time()
        self.previous_time = 0

        self.task_previous_times = self.task_manager.get_usages( self.active_task_name )

        # with self.lock : 
        self.update_timer() 


        
    
    def update_timer_label( self ) :
        
        hours, mins = divmod( self.elapsed, 60 ) 
        
        label = '%d:%s' % ( int( hours ), str( int( mins ) ).zfill(2) )
        self.label.setText( label ) 

        label_icon_path = gui_config.data_path + 'label_icon.png'
        
        # create image
        img = Image.new('RGBA', (400, 200), color = (255, 255, 255, 0 ))  # color background =  white  with transparency
        d = ImageDraw.Draw(img)

        font_type  = ImageFont.truetype( "Arial.ttf", 200 )

        if self.running :
            fill = ( 11, 186, 41, 255 )
        else :
            fill = ( 217, 15, 27, 255 )

        # fill = ( 0, 0, 0, 255 ) 
        
        d.text(( 0,0), label, fill = fill, font = font_type)
        
        img.save( label_icon_path )

        icon = QIcon( label_icon_path ) 
        
        self.tray.setIcon( icon ) 



    def update_timer( self ) :
                    
        # compute timer time in seconds 
        elapsed = time.time() - self.start_time + self.previous_time

        # convert elapsed to minutes. to debug and use seconds, comment this out
        if not USE_SECONDS : 
            elapsed /= 60

        self.elapsed = elapsed 

        # track task time in hours
        task_name = self.active_task_name 
        new_usages = self.task_previous_times + elapsed / 60
        self.controller.task_manager.set_usages( task_name, new_usages )

        self.timer_updated_signal.emit() 


        
    def update_timer_target( self ) :

        while 1 :

            if self.running :

                with self.lock :
                    self.update_timer() 

                if USE_SECONDS : 
                    time.sleep( 0.2 )

                else :
                    time.sleep( 5 ) 
