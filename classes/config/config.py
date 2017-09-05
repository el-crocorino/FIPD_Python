# coding: utf8
# config object

from classes.db_object import db_object

class config(db_object):

	"""Handles FIPD app config"""

	def __init__(self):
		super(config, self).__init__('config', ['id', 'name', 'value', 'created_date', 'updated_date'])

	def load(self, data):

		self.id = data[0]
		self.name = data[1]
		self.value = data[2]
		self.created_date = data[3]
		self.updated_date = data[4]
