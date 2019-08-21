from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

import numpy as np 
import datetime

import gui_config
from time_transaction import TimeTransaction



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

		add_transaction_button = QPushButton( '+' )
		add_transaction_button.clicked.connect( 
			self.add_transaction_button_clicked )
		hlayout.addWidget( add_transaction_button ) 


		delete_transaction_button = QPushButton( '-' )
		delete_transaction_button.clicked.connect( 
			self.delete_transaction_button_clicked )
		hlayout.addWidget( delete_transaction_button ) 


		layout.addLayout( vlayout ) 


	def add_transaction_button_clicked( self ) : 
		self.dialog = AddTransactionDialog( self.controller ) 
		self.dialog.show()

		# add_pressed, transaction = self.dialog.get_response()

		# if add_pressed : 
		# 	print(1)
		# else : 
		# 	print( 2 )


	def delete_transaction_button_clicked( self ) : 
		print( 'clicked' )


	# append = 1 -> insert new row at top of table. else update the specified row. 
	def add_transaction_to_table( self, transaction, append = 1, row = 0 ) : 

		task_name   = QLabel( transaction.task_name )		
		
		time_format = '%H:%M:%S'
		date_format = '%m/%d/%Y'

		start_time = QLabel( transaction.start_time.strftime( time_format ) )
		stop_time  = QLabel( transaction.stop_time.strftime(  time_format ) )

		if append : 
			row = 0
			self.table.insertRow( row )

		self.table.setCellWidget( 0, 0, task_name )
		self.table.setCellWidget( 0, 1, start_time )
		self.table.setCellWidget( 0, 2, stop_time )
		


	def get_transaction( self ) : 
		... 


	# make sure a proposed transaction is valid with the current table 
	def check_consistency( self, transaction ) : 
		...




class TransactionDialog( QDialog ) : 


	def __init__( self, controller ) :
		super().__init__() 

		self.controller = controller
		self.add_pressed = 0 

		# disable blocking of main app 
		self.setWindowModality( Qt.NonModal )
		# self.setWindowModality(QtCore.Qt.WindowModal)
		self.setWindowTitle( 'Add Transaction' ) 

		layout = QFormLayout()

		self.task_name_combobox = QComboBox()
		task_names = self.controller.task_manager.get_task_names()
		self.task_name_combobox.addItems( task_names )
		layout.addRow( 'Task Name', self.task_name_combobox )

		self.start_time_widget = QDateTimeEdit( datetime.datetime.now() )
		layout.addRow( 'Start Time', self.start_time_widget )

		self.stop_time_widget = QDateTimeEdit( datetime.datetime.now() )
		layout.addRow( 'Stop Time', self.stop_time_widget )

		self.add_button = QPushButton( 'Add' )
		# add_button.clicked.connect( self.add_button_clicked )
		layout.addRow( self.add_button ) 

		self.setLayout( layout ) 


	def get_response( self ) : 
		
		task_id = -1	# assigned later
		task_name = self.task_name_combobox.currentText()
		start_time = self.start_time_widget.dateTime().toPyDateTime() 
		stop_time = self.stop_time_widget.dateTime().toPyDateTime() 

		transaction = TimeTransaction( task_id, task_name, start_time, stop_time )

		return transaction






class AddTransactionDialog( TransactionDialog ) :

	def __init__( self, controller ) : 
		super().__init__( controller ) 
		self.add_button.clicked.connect( self.add_button_clicked )


	def add_button_clicked( self ) : 
		# self.add_pressed = 1 
		transaction = self.get_response()
		task_id = self.controller.time_transaction_manager.db.get_unique_task_id() 
		transaction.task_id = task_id

		self.controller.time_transaction_widget.add_transaction_to_table( transaction )
		self.controller.time_transaction_manager.db.insert_transaction( transaction ) 

		self.close()




class EditTransactionDialog( TransactionDialog ) : 

	def __init__( self, controller ) : 
		super().__init__( controller )
		self.add_button.clicked.connect( self.add_button_clicked )


	def add_button_clicked( self ) : 
		# self.add_pressed = 1 
		
		transaction = self.get_response()

		#todo 
		# self.controller.add

		self.close()
