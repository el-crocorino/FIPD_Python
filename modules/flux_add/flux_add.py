# coding: utf8
# Add Flux Module

import os
import config

from classes.flux.flux import flux
from classes.flux.flux_manager import flux_manager

class flux_add():

	def __init__(self):
		self.conf = config.get_conf()

	def run(self):

		name = input('Please enter new show name : ')
		url = input('Please enter show rss adress : ')
		keywords = input('Please enter show keywords, if any : ')

		new_flux = flux(name, url, keywords)
		new_flux_directory = self.conf['download_dir'] + '/' + new_flux.name

		if not os.path.exists(new_flux_directory):
			os.makedirs(new_flux_directory)

		new_flux.save([new_flux.__dict__])

		return [True, True, '', True]

