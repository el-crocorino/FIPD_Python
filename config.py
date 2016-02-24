# config

import os

conf = {}

conf['dir'] 			= os.path.dirname(os.path.realpath(__file__))
conf['download_dir'] 	= ''

conf['db_name'] = 'fipd.db'
conf['db_path'] = conf['dir'] + '/sql/' + conf['db_name']

def get_conf():
	return conf
