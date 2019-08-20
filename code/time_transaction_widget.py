from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5 import QtCore

import numpy as np 

import gui_config



class TimeTransaction( object ) :

	def __init__( self, task_id = -1, task_name = None, 
		start_time = None, end_time = None ) : 

		self.task_id = task_id
		self.task_name = task_name 
		self.start_time = start_time 
		self.end_time = end_time 

 

class TimeTransactionWidget( QWidget ) :
# class TaskTableManager( QWidget ) :
	
	def __init__( self, controller ) :
		super().__init__()
		self.controller = controller


	def init( self ) :

		toplayout = QHBoxLayout()
		self.setLayout( toplayout )

		box = QGroupBox( 'Time Transactions' )
		layout = QVBoxLayout()
		box.setLayout( layout ) 
		toplayout.addWidget( box )
		
		vlayout = QVBoxLayout()

		table_labels = [ 'Task Name', 'Start Time', 'End Time', ]
		nrows = gui_config.DEFAULT_NUM_TRANSACTIONS
		ncols = len( table_labels )
		self.table = QTableWidget( nrows, ncols )

		self.table.setColumnWidth( 0, 200 )
		self.table.setColumnWidth( 1, 80 )
		self.table.setColumnWidth( 2, 80 )

		vlayout.addWidget( self.table ) 


		hlayout = QHBoxLayout()
		vlayout.addLayout( hlayout )

		add_transaction_button = QPushButton( 'Add Transaction' )
		add_transaction_button.clicked.connect( 
			self.add_transaction_button_clicked )
		hlayout.addWidget( add_transaction_button ) 


		delete_transaction_button = QPushButton( 'Add Transaction' )
		delete_transaction_button.clicked.connect( 
			self.delete_transaction_button_clicked )
		hlayout.addWidget( delete_transaction_button ) 


		layout.addLayout( vlayout ) 


	def add_transaction_button_clicked( self ) : 
		print( 'clicked' )
		

	def delete_transaction_button_clicked( self ) : 
		print( 'clicked' )


	def add_transaction_to_table( self, transaction, row = 0 ) : 

		task_name   = QLabel(         transaction.task_name  )		
		start_entry = QLineEdit( str( transaction.start_time ) )
		stop_entry  = QLineEdit( str( transaction.stop_time  ) )

		if append : 
			row = 0
			self.table.insertRow( row )



	def get_transaction( self ) : 
		... 


	# make sure a proposed transaction is valid with the current table 
	def check_consistency( self, transaction ) : 
		...





class AddTransactionDialog( QDialog ) :

    def __init__( self ) :
        super().__init__() 

        # disable blocking of main app 
        self.setWindowModality( Qt.NonModal )
        
        self.setWindowTitle( 'Plot Actions' ) 

        layout = QVBoxLayout()

        save_plot_button = QPushButton( 'Save Plot' ) 
        # todo 
        layout.addWidget( save_plot_button ) 

        # save gif / movie interface 
        tmplayout = QHBoxLayout()

        movie_type_combobox = QComboBox()
        for movie_type in MOVIE_TYPES :
            movie_type_combobox.addItem( movie_type ) 
            tmplayout.addWidget( movie_type_combobox )
        
        start_frame_entry = QLineEdit( '' )
        start_frame_entry.setPlaceholderText( 'Start Frame' ) 
        start_frame_entry.setToolTip( 'Start Frame' ) 
        tmplayout.addWidget( start_frame_entry ) 
        
        stop_frame_entry = QLineEdit() 
        stop_frame_entry.setToolTip( 'stop frame' )
        stop_frame_entry.setPlaceholderText( 'stop frame' ) 
        tmplayout.addWidget( stop_frame_entry )

        frame_stride_entry = QLineEdit()
        frame_stride_entry.setToolTip( 'Frame stride' ) 
        frame_stride_entry.setPlaceholderText( 'Frame stride' ) 
        tmplayout.addWidget( frame_stride_entry ) 
        
        frame_rate_entry = QLineEdit( str(1) )
        frame_rate_entry.setToolTip( 'Frame Rate in Hz' ) 
        tmplayout.addWidget( frame_rate_entry ) 
        
        save_movie_button = QPushButton( 'Save' )
        tmplayout.addWidget( save_movie_button  )
        
        layout.addLayout( tmplayout  )  

        self.setLayout( layout ) 
