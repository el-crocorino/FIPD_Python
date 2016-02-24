# config object

from classes.db_object import db_object

class config(db_object):

	"""Handles FIPD app config"""

	def __init__(self):
		super(config, self).__init__('config', ['id', 'name', 'value', 'created_date', 'updated_date'])

	def load(self, data):

		self.id = data[0]
		self.remote_id = data[1]
		self.flux_id = data[2]
		self.title = data[3]
		self.url = data[4]
		self.diffusion_date = data[5]
		self.download_date = data[6]
		self.status = data[7]
