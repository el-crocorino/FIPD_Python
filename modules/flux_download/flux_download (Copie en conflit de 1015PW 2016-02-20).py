# flux download

import requests
import urllib
import time
import datetime

import config

from lxml import etree

from classes.flux.flux import flux
from classes.flux.flux_manager import flux_manager
from classes.show.show import show
from classes.show.show_manager import show_manager

# from modules.show_download.show_download import show_download

class flux_download():

	"""download flux from url"""

	def __init__(self):
		self.conf = config.get_conf()

	def run(self):

		flux_id = input('Please insert the id of the show you want to download : ')

		self.flux_mng = flux_manager()
		self.flux = self.flux_mng.get_by_id(flux_id)

		self.show_list = []
		self.load_xml()
		self.download_show_list()

		return True

	def load_xml(self):

		tree = etree.parse(self.flux.url)
		self.xml_root = tree.getroot()

		for item in self.xml_root.iter('item'):

			show_data = []
			if self.flux.keywords != None and len(self.flux.keywords) != 0:
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

	def get_show_data(self, xml_item):

			show_data =  [
				None,
				xml_item.find('podcastRF:magnetothequeID', self.flux.namespaces).text,
				self.flux.id,
				xml_item.find('title').text,
				xml_item.find('guid').text,
				xml_item.find('pubDate').text,
				None,
				'remote',
			]

			return show_data

	def download_show_list(self):

		self.show_mng = show_manager()
		show_dict = self.show_mng.get_all_by_remote_id()

		for show in self.show_list:

			timestamp = time.mktime(time.strptime(show.diffusion_date, '%a, %d %b %Y %H:%M:%S +0100'))
			show_diff_date = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')

			show_path = self.conf['dir'] + '/Downloads/' + self.flux.name + '/' + show_diff_date + ' - ' + self.flux.name + ' - ' + show.title + '.mp3'

			if show.remote_id in show_dict and show_dict[show.remote_id].status == 'downloaded':
			 	print('This show has already been downloaded on ', show_dict[show.remote_id].download_date)
			else :
				try:

					# import urllib
					# urllib.urlretrieve (show.url, show_path)


					# self.download_file(show, show_path)


					import urllib.request
					import shutil

					print(test)

					# Download the file from `url` and save it locally under `file_name`:
					response = urllib.request.urlopen(show.url)
					out_file = open(show_path, 'wb')

					print(response)
					print(out_file)

					shutil.copyfileobj(response, out_file)

					print('kikoo')
					print(show_path)

					show.status = 'downloaded'

				except:
					show.status = 'error'

				show.download_date = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
				# self.show_mng.save([show.__dict__])

	# def download_file(self, show, show_path):

	# 	import urllib2

	# 	url = show.url

	# 	file_name = show_path
	# 	u = urllib2.urlopen(url)
	# 	f = open(file_name, 'wb')
	# 	meta = u.info()
	# 	file_size = int(meta.getheaders("Content-Length")[0])

	# 	print "Downloading: %s Bytes: %s" % (file_name, file_size)

	# 	file_size_dl = 0
	# 	block_sz = 8192

	# 	while True:

	# 	    buffer = u.read(block_sz)

	# 	    if not buffer:
	# 	        break

	# 	    file_size_dl += len(buffer)
	# 	    f.write(buffer)
	# 	    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
	# 	    status = status + chr(8)*(len(status)+1)

	# 	    print status,

	# 	f.close()




