# flush database Module

from classes.config.config_manager import config_manager
from classes.flux.flux_manager import flux_manager
from classes.show.show_manager import show_manager

class database_flush():

	def __init__(self):
		pass

	def run(self):

		validation = input('You will lose every record of show or emission you have downloaded until now. Are you sure you want to proceed (y/n) ?')

		if validation.upper() == 'Y':
			flux_mng = flux_manager()
			flux_mng.flush()
			show_mng = show_manager()
			show_mng.flush()
			config_mng = config_manager()
			config_mng.flush()

			# TODO add new definition of daownload dir

		return [True, True, 'Database flushed.']
