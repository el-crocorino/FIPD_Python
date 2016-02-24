# config manager

from classes.db_object import db_object
from classes.config.config import config

class config_manager(db_object):

	def __init__(self):
		super(config, self).__init__('config', ['id', 'name', 'value', 'created_date', 'updated_date'])

	def get_all(self, where = {}):

		rows = super(config_manager, self).get_all(where)

		items = []

		print(rows)

		for row in rows:

			self.get_class('classes.' + self.table)

			new_config = config()
			new_config.load(row)
			items.append(new_config)

		return items

	def get_item(self, item):
		item = self.get_all({'config_name', item})



