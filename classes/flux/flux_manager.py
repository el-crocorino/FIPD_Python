# coding: utf8
# flux manager

from classes.db_object import db_object
from classes.flux.flux import flux

class flux_manager(db_object):

	def __init__(self):
		super(flux_manager, self).__init__('flux', ['name', 'url', 'keywords', 'created_date', 'updated_date'])

	def get_all( self, where = {}):

		rows = super( flux_manager, self).get_all(where, 0, '')

		items = []

		for row in rows:

		    self.get_class( 'classes.' + self.table)

		    new_flux = flux()
		    new_flux.load( row)
		    items.append( new_flux)

		return items
	
	def get_by_id( self,fluxId):		
		
		row = super( flux_manager, self).get_by_id( fluxId)		
	
		new_flux = flux()
		new_flux.load( row)		
		
		return new_flux


