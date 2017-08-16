# show manager

from classes.db_object import db_object
from classes.show.show import show

class show_manager(db_object):

	def __init__(self):
		super(show_manager, self).__init__('show', ['remote_id', 'flux_id', 'title', 'url', 'diffusion_date', 'download_date', 'status'])

	def get_all(self, params, maxLimit):

		rows = super(show_manager, self).get_all(params, maxLimit)

		items = []

		for row in rows:

		    self.get_class('classes.' + self.table)

		    new_show = show()
		    new_show.load(row)
		    items.append(new_show)

		return items

	def	get_all_by_remote_id(self):

		show_list = self.get_all({}, 70)
		show_dict = {}

		for show in show_list:
			show_dict[show.remote_id] = show

		return show_dict

	def get_show_by_remote_id(self, remote_id):

		show_data = self.get_all({'remote_id' : remote_id})

		if show_data != None:
			self.load(show_data[0])
			return show

		return False
