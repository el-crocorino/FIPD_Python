# coding: utf8
# update Flux Module

import datetime
import json
import sys

from classes.flux.flux import flux
from classes.flux.flux_manager import flux_manager

class flux_update():

	def __init__(self):
		pass

	def run(self):

		flux_id = int(input('Please insert the id of the show you want to update : '))

		flux_mng = flux_manager()
		flux = flux_mng.get_by_id(flux_id)

		return self.update_flux_infos(flux)

	def update_flux_infos(self, flux):

		print('Shows informations : ')

		action = input('Update (N)ame, (U)rl, (K)eywords, or (B)ack to shows list? ').upper()

		if action == 'B':
			return True
		else:
			if action == 'N':
				flux.name = name = input('Please enter show\'s new name : ')
			elif action == 'U':
				flux.url = input('Please enter show\'s new rss adress : ')
			elif action == 'K':
				print('Current keywords are : ', flux.keywords)
				keywords_string = input('Please enter show\'s new comma-separated keywords list, or press (R) to reset keywords list : ')

				new_keywords = []

				if keywords_string.upper() != 'R':

					if flux.keywords != None:
						new_keywords = flux.keywords

					keywords_array = keywords_string.split(',')

					for word in keywords_array:
						new_keywords.append(word.strip())

				flux.keywords = new_keywords

			flux.keywords = json.dumps(flux.keywords, separators = (',', ':')).encode('utf8')
			flux.updated_date = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

			flux.save([flux.__dict__])

		return [True, True, '', True]

