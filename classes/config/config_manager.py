# config manager

import datetime

from classes.db_object import db_object
from classes.config.config import config

class config_manager(db_object):

	def __init__(self):
		super(config_manager, self).__init__('config', ['id', 'name', 'value', 'created_date', 'updated_date'])
		self.storable_items = [
			'download_dir',
		]

	def get_all(self, where = {}):

		rows = super(config_manager, self).get_all(where, 0)

		items = []

		for row in rows:

			self.get_class('classes.' + self.table)

			new_config = config()
			new_config.load(row)
			items.append(new_config)

		return items

	def get_all_items(self):
		items = self.get_all()

		config = {}
		for item in items:
			config[item.name] = item.value

		return config

	def get_item(self, item):
		item = self.get_all({'config_name', item})

	def save(self, conf):

		conf_list = self.get_all()

		if any(conf_list):
			for conf_item in conf_list:
				self.update_conf_item(conf, conf_item)
		else:
			for item in self.storable_items:
				conf_item = config()
				conf_item.id = None
				conf_item.name = item
				conf_item.created_date ='{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
				self.update_conf_item(conf, conf_item)

	def update_conf_item(self, conf, conf_item):

		conf_item.updated_date ='{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

		for item in self.storable_items:
			if conf_item.name == item and conf[item] != None:
				conf_item.value = conf[item]
				super(config_manager, self).save([conf_item.__dict__])



