# coding: utf8
# flux download

import datetime
import os
import re
import requests
import sys
import time
import unicodedata
import urllib

import config

from lxml import etree
from time import sleep
from urllib.request import urlopen

from classes.flux.flux import flux
from classes.flux.flux_manager import flux_manager
from classes.show.show import show
from classes.show.show_manager import show_manager

class flux_download():

	"""download flux from url"""

	def __init__(self):
		self.conf = config.get_conf()

	def run(self, flux_id = None):

		if flux_id == None:
			try:
				flux_id = int(input('Please insert the id of the show you want to download : '))
			except ValueError:
				print('Please insert an integer as show id')
				self.run()

		self.flux_mng = flux_manager()		
		self.flux = self.flux_mng.get_by_id(flux_id)

		self.show_list = []
		XMLLoading = self.load_xml()
		
		if( XMLLoading):

			try :
				download_list = self.download_show_list()
				report = 'Download report for ' + self.flux.name + ': ' + download_list
				return [True, True, report, True]
			except Exception as e:
				print(e)
		else:
			return [True, False, 'Le flux n\'est pas accessible', True]

	def load_xml(self):
		
		try:
			ret = requests.head(self.flux.url)
		except requests.exceptions.ConnectionError as e:
			return False
		
		tree = etree.parse(self.flux.url)
		self.xml_root = tree.getroot()

		for item in self.xml_root.iter('item'):

			show_data = []
			if self.flux.keywords != None and len(self.flux.keywords) != 0:
				'''
				k = ''
				for keyword in self.flux.keywords:
					k = k + ' ' + keyword
				'''
				
				itemTitle = item.find('title').text
				# DebugKeyWordCheck = any(keyword in item.find('title').text for keyword in self.flux.keywords)
				if any(keyword in item.find('title').text for keyword in self.flux.keywords):
					show_data = self.get_show_data(item)
					new_show = show()
					new_show.load(show_data)

					self.show_list.append(new_show)
			else:
				show_data = self.get_show_data(item)
				new_show = show()
				new_show.load(show_data)

				self.show_list.append(new_show)
				
		self.getOldestShowTimestamp()
		
		return True

	def get_show_data(self, xml_item):

			show_data =  [
				None,
				xml_item.find('podcastRF:magnetothequeID', self.flux.namespaces).text,
				self.flux.id,
				xml_item.find('title').text,
				xml_item.find('guid').text,
				xml_item.find('pubDate').text,
				time.mktime(time.strptime(xml_item.find('pubDate').text, '%a, %d %b %Y %H:%M:%S ' + xml_item.find('pubDate').text[-5:])),
				None,
				'remote',
			]

			return show_data
		
	def getOldestShowTimestamp(self):
		
		if not self.show_list:
			pass
		else:		
			latestShow = self.show_list[-1]
			self.oldestShowTimestamp = time.mktime(time.strptime(latestShow.diffusion_date, '%a, %d %b %Y %H:%M:%S ' + latestShow.diffusion_date[-5:]))

	def download_show_list(self):
		
		if not self.show_list:
			
			k = ''
			for keyword in self.flux.keywords:
				k = k + ' ' + keyword
			download_report = '\n\tNo new podcast matching keywords (' + k + ' ) for ' + self.flux.name + '.'
			
		else:

			self.show_mng = show_manager(self.flux.id)
			show_dict = self.show_mng.get_all_by_remote_id({'diffusion_timestamp': self.oldestShowTimestamp}) 
	
			download_report = ''		
		
			showsDownloadList = []
			for show in self.show_list:
				if show.remote_id in show_dict and show_dict[show.remote_id].status == 'downloaded':
					pass
				else:
					showsDownloadList.append(show)
			
			self.fileCounter = 1
			self.filesCount = len(showsDownloadList)
			
			if not showsDownloadList:
				download_report += '\n\tNo new podcast available for ' + self.flux.name + '.'
			else:
				for show in showsDownloadList:
					
					# Dates
					timestamp = time.mktime(time.strptime(show.diffusion_date, '%a, %d %b %Y %H:%M:%S ' + show.diffusion_date[-5:]))		
					show.diffusion_date = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S' + show.diffusion_date[-5:])
					show_diff_date = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')
		
					# Filname & path
					show_filename = show_diff_date + '_' + self.get_valid_filename(self.flux.name + '_' + show.title)
					if len(show_filename) > 65:
						show_filename = show_filename[:65]				
					show_filename += '.mp3'
					show_path = self.conf['download_dir'] + '/' + self.flux.name + '/' + show_filename
		
					show.status = 'error'
					
					try:
					
						remote_file_size = self.download_file(show, show_path)
		
						if remote_file_size == os.stat(show_path).st_size:
							show.status = 'downloaded'
		
					except Exception as e:
						print(e)
		
					show.download_date = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
					self.show_mng.save([show.__dict__])
					self.fileCounter = self.fileCounter+1
					
					download_report += '\n\t' + show_filename + ' - ' + show.status

		return download_report

	def download_file(self, show, show_path):

		url = show.url

		file_name = show_path
		u = urlopen(url)
		f = open(file_name, 'wb')
		meta = u.info()
	
		file_size = int(meta.get_all("Content-Length")[0])
		baseText = 'Downloading ' + self.flux.name[:8] + '... ' + str(self.fileCounter) + '/' + str(self.filesCount) + ': ' + show.diffusion_date[0:10] + ' ' + show.title[:27] + '. ' + str(file_size / 1000000)[:5] + ' Mo'

		file_size_dl = 0
		block_sz = 1000000

		while True:

			try :
				buffer = u.read(block_sz)

				if not buffer:
					break

				file_size_dl += len(buffer)
				f.write(buffer)
				
				status = r"  [%3.2f%%]" % (file_size_dl * 100. / file_size)
				status = baseText + status + chr(8)*(len(baseText + status)+1)

				sys.stdout.write('\r')
				sys.stdout.write(status)
				sys.stdout.flush()
				sleep(0.25)

				print(status, end="")

			except Exception as e:
				print(e)

		f.close()		

		return file_size
	
	def get_valid_filename(self, value):
		"""
		copied fromDjango django/utils/text.py slugify() method
		"""
		value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
		value = re.sub('[^\w\s-]', '', value).strip().lower()
		return re.sub('[-\s]+', '-', value)


