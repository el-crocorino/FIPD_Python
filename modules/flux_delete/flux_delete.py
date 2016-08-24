# delete Flux Module

from classes.flux.flux import flux
from classes.flux.flux_manager import flux_manager

class flux_delete():

	def __init__(self):
		pass

	def run(self):

		flux_id = input('Please enter show id : ')

		flux_mng = flux_manager()
		flux = flux_mng.get_by_id(flux_id)
		flux_mng.delete(flux.__dict__)

		return [True, True, '', True]
