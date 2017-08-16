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
from modules.fluxs_download.fluxs_download import fluxs_download
from modules.database_flush.database_flush import database_flush
from modules.settings_update.settings_update import settings_update

import sql.db_build

class app():
	"""FIPD Application"""

	def __init__(self):
		self.conf = config.get_conf()

	def initialize(self):

		# Check if database exists, if not : creates it
		if not os.path.isfile(self.conf['dir'] + '/sql/' + self.conf['db_name']):
			sql.db_build.main()

		# import database stored config data
		config_mng = config_manager()
		config_items = config_mng.get_all_items()

		if any(config_items) :
			for key, value in config_items.items():
				self.conf[key] = value

		# Check download dir
		if self.conf['download_dir'] == None or self.conf['download_dir'] == '':
			self.conf['download_dir'] = input('Please enter full path to download folder: ')
			config_mng.save(self.conf)


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

	def route(self, clear = True, message = '', display_list = False):

		if clear:
			os.system('cls' if os.name == 'nt' else 'clear')

		if message != '':
			print(message)

		if display_list:
			print('\n\nYou can currently download podcasts from the following shows : \n' + self.print_flux_list() + '\n\nAvailable actions: \n\t- (D)ownload a show;\n\t- (A)dd a show;\n\t- (U)pdate a show;\n\t- (R)emove a show;\n\t- Download (E)very available shows;\n\t- Update (S)ettings;\n\t- (F)lush the database;\n\t- (Q)uit.')

		action = input('Please enter action letter : ').upper()

		module = None

		if action == 'Q':
			os.system('cls' if os.name == 'nt' else 'clear')
			exit()
		elif action == 'F':
			module = database_flush()
		elif action == 'A':
			module = flux_add()
		elif action == 'R':
			module = flux_delete()
		elif action == 'U':
			module = flux_update()
		elif action == 'D':
			module = flux_download()
		elif action == 'E':
			module = fluxs_download()
		elif action == 'S':
			module = settings_update()

		if module != None:
			action = module.run()
		else:
			self.route(False, 'Unknown action, please retry.', False)
			
		if action[0]:
			self.route(action[1], action[2], action[3])

