# show object

import time
from classes.db_object import db_object

class show(db_object):

	"""Handles radio shows"""

	def __init__(self):
		super(show, self).__init__('show', ['remote_id', 'flux_id', 'title', 'url', 'diffusion_date', 'diffusion_timestamp', 'download_date', 'status'])

	def load(self, data):

		self.id = data[0]
		self.remote_id = data[1]
		self.flux_id = data[2]
		self.title = data[3]
		self.url = data[4]
		self.diffusion_date = data[5]
		self.diffusion_timestamp = data[6]
		self.download_date = data[7]
		self.status = data[8]
