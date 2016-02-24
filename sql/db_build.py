# db_build

import config
import sqlite3

def main():

	conf = config.get_conf()
	connexion = start_db_connection(conf)

	create_config_table(connexion)
	create_flux_table(connexion)
	create_show_table(connexion)

	close_db_connection(connexion)

def start_db_connection(conf):
	conn = sqlite3.connect(conf['db_path'])
	return conn

def close_db_connection(conn):
	conn.close()

def create_config_table(conn):
	"""2016-02-24 - Create config table"""

	cursor = conn.cursor()
	cursor.execute("""CREATE TABLE IF NOT EXISTS config(
			config_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
		    config_name TEXT,
		    config_value TEXT,
		    config_created_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
		    config_updated_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
		)""")
	conn.commit()

	config = []
	config.append(('download_dir', None))
	cursor.executemany("""INSERT INTO config(config_name, config_value) VALUES(?, ?)""", config)
	conn.commit()

def create_flux_table(conn):
	"""2016-02-08 - Create flux table"""

	cursor = conn.cursor()
	cursor.execute("""CREATE TABLE IF NOT EXISTS flux(
			flux_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
		    flux_name TEXT,
		    flux_url TEXT,
		    flux_keywords TEXT,
		    flux_created_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
		    flux_updated_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
		)""")
	conn.commit()

def create_show_table(conn):
	"""2016-02-08 - Create show table"""

	cursor = conn.cursor()
	cursor.execute("""CREATE TABLE IF NOT EXISTS show(
			show_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
		    show_remote_id TEXT,
			show_flux_id INTEGER,
		    show_title TEXT,
		    show_url TEXT,
		    show_diffusion_date DATETIME,
		    show_download_date DATETIME,
		    show_status TEXT
		)""")
	conn.commit()

	# http://radiofrance-podcast.net/podcast09/rss_14007.xml

