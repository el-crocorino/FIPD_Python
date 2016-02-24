# FIPD App

import config
import os

from classes.config.config_manager import config_manager
from classes.show.show import show
from classes.show.show_manager import show_manager
from classes.flux.flux import flux
from classes.flux.flux_manager import flux_manager

from modules.flux_add.flux_add import flux_add
from modules.flux_delete.flux_delete import flux_delete
from modules.flux_update.flux_update import flux_update
from modules.flux_download.flux_download import flux_download
from modules.database_flush.database_flush import database_flush

import sql.db_build

class app():
	"""FIPD Application"""

	def __init__(self):
		self.conf = config.get_conf()

	def initialize(self):

		if not os.path.isfile(self.conf['dir'] + '/sql/' + self.conf['db_name']):
			sql.db_build.main()

		config_mng = config_manager()
		download_dir = config_mng.get_item('download_dir')

		if download_dir == None:
			download_dir = input('Please enter full path to download folder: ')

		self.conf['download_dir'] = download_dir

	def print_flux_list(self):

		flux_mng = flux_manager()
		flux_list = flux_mng.get_all()

		flux_list_string = ''

		for flux in flux_list:
			flux_list_string += '\n\t(' + str(flux.id) + ') - ' + flux.name + ' (last update : ' + flux.updated_date + ')'

		if flux_list_string == '':
			flux_list_string = '\n\tNo show available yet.'

		return flux_list_string

	def welcome(self):

		print('\n\nWelcome to the France Inter Podcast Downloader.')

	def route(self, clear = True, message = ''):

		if clear:
			os.system('cls' if os.name == 'nt' else 'clear')

		if message != '':
			print(message)

		print('\n\nYou can currently download podcasts from the following shows : \n' + self.print_flux_list() + '\n\nYou can (D)ownload, (A)dd, (U)pdate or (R)emove a show.\n\nYou can also (F)lush the entire database to take a fresh new start, or simply (Q)uit.')

		action = input('Please enter action letter : ').upper()

		module = None

		if action == 'Q':
			os.system('cls' if os.name == 'nt' else 'clear')
			exit()
		elif action == 'A':
			module = flux_add()
		elif action == 'R':
			module = flux_delete()
		elif action == 'U':
			module = flux_update()
		elif action == 'D':
			module = flux_download()
		elif action == 'F':
			module = database_flush()

		if module != None:
			action = module.run()

		if action[0]:
			self.route(action[1], action[2])

