__author__ = 'Mark Mon Monteros'

import cv2, os, sys, subprocess
import pandas as pd
from pyzbar.pyzbar import decode
from pathlib import Path
from datetime import datetime
from pytz import timezone

class SurnecoWarehouse():

	def __init__(self):
		self.now = datetime.now(timezone('Asia/Manila'))
		self.current_date = self.now.strftime('%m-%d-%Y')
		self.current_time = self.now.strftime('%H-%M')
		self.master_dbfile = ''
		self.filename = 'SURNECO Warehouse Inventory_' + self.current_date + '_' + self.current_time + '.csv'
		self.master_output_folder = Path.cwd().joinpath('reports')
		self.master_output_file = self.master_output_folder.joinpath(self.filename)
		self.dump_folder = self.master_output_folder.joinpath('dump').joinpath(self.current_date)
		self.dump_file = self.dump_folder.joinpath(self.filename)
		self.input_barcode = 'Img.jpg' # for test / change to input img
		self.isItem = None

		self.getBarcode()

	def getBarcode(self):
		self.barcode_img = cv2.imread(self.input_barcode)
		detectedBarcodes = decode(self.barcode_img)
	
		if not detectedBarcodes:
			print('\nBarcode Not Detected or your barcode is blank/corrupted!')
			sys.exit(1)
		else:
			for barcode in detectedBarcodes:
				(x, y, w, h) = barcode.rect
				
				cv2.rectangle(self.barcode_img, (x-10, y-10),
							(x + w+10, y + h+10),
							(255, 0, 0), 2)
				
				if barcode.data != '':
					self.data = barcode.data
					self.type = barcode.type

		self.generateReport()

	def generateReport(self):
		# Check if reports folder exist
		if not Path.exists(self.master_output_folder):
			os.mkdir(self.master_output_folder)
		# Check if dumps folder exist
		if not Path.exists(self.master_output_folder.joinpath('dump')):
			os.mkdir(self.master_output_folder.joinpath('dump'))

		master_files = []

		for f in os.listdir(self.master_output_folder):
			if f.endswith('.csv'):
				if f.startswith('SURNECO'):
					master_files.append(self.master_output_folder.joinpath(f))

		if len(master_files) != 0:
			latest_file = max(master_files, key=os.path.getctime)
			self.master_dbfile = latest_file

			print('\nMaster Database: ', str(os.path.basename(self.master_dbfile)))

			for f in master_files:
				if f is not self.master_dbfile:
					os.remove(self.master_output_folder.joinpath(f))

		try:
			with open (self.master_dbfile, 'r', encoding='UTF-8') as latest_db:
				df = pd.read_csv(latest_db)
		except:
			print('\nNo Master Database Found!')
			print('\nCreating New Database...')
			df = pd.DataFrame(columns=['Product Name', 'Quantity', 'Code', 'Type'])

		print('\nUpdating Database...')
		
		for self.data in df['Code']:
			self.isItem = True

		if self.isItem:
			# Item exists
			df['Quantity'] = df['Quantity'] + 1
		else:
			# Item does not exist
			new_entry = ['Generator', 1, self.data, self.type]
			df.loc[len(df)] = new_entry

		# MASTER DB FILE
		if self.master_dbfile:
			os.remove(self.master_dbfile)

		df.to_csv(self.master_output_file, index=False, encoding='UTF-8')

		# DUMP FILES
		try:
			os.mkdir(self.dump_folder)
		except:
			pass

		df.to_csv(self.dump_file, index=False, encoding='UTF-8')

		# self.displayImage()
		# self.openReport()

	def openReport(self):
		print('\nOpening File...')
		if sys.platform == 'win32':
			os.startfile(self.master_output_file)
		else:
			opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
			subprocess.call([opener, self.master_output_file])

	def displayImage(self):
		print('\nOpening Image...')
		cv2.imshow('Image', self.barcode_img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

if __name__ == '__main__':
    print('\n>> SURNECO Warehouse Inventory <<')
    print('\nCreated by: ' + __author__)
    
    SurnecoWarehouse()
    
    print('\n\nDONE...!!!\n')
