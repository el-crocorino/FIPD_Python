# flux object
# coding: utf8
# -*- coding: utf-8 -*-

import datetime
import json
from classes.db_object import db_object

class flux(db_object):

	"""Handles radio fluxs"""

	def __init__(self, name = None, url = None, keywords = None):

		super(flux, self).__init__('flux', ['name', 'url', 'keywords', 'created_date', 'updated_date'])

		self.id = None
		self.name = name
		self.url = url

		self.keywords = None

		if keywords != None and keywords != '':
			self.add_keywords(keywords)

		self.created_date = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
		self.updated_date = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

	def load(self, data):

		self.id = data[0]
		self.name = data[1]
		self.url = data[2]

		if data[3] != None and data[3] != '':
		# if data[3] != None:    # TODO : Make sure that empty keywords are stored as NULL in database
			try:
				self.keywords = json.loads(data[3].decode('utf8'))
			except AttributeError:
				self.keywords = json.loads(data[3])
		else:
			self.keywords = []

		self.created_date = data[4]
		self.updated_date = data[5]

	def add_keywords(self, keywords):

		new_keywords = []

		if self.keywords != None:
			new_keywords = self.keywords

		keywords_array = keywords.split(',')

		for word in keywords_array:
			new_keywords.append(word.strip())

		self.keywords = json.dumps(new_keywords, separators = (',', ':'))



