#!/usr/bin/python3
# FIPD
from classes.app import app
from classes.show import show
from classes.flux import flux

# Masque : http://radiofrance-podcast.net/podcast09/rss_14007.xml
# Gallienne : http://radiofrance-podcast.net/podcast09/rss_11262.xml
# Affaires sensibles : http://radiofrance-podcast.net/podcast09/rss_13940.xml

def main():

	FIPD = app()
	FIPD.initialize()
	FIPD.welcome()
	FIPD.route(False, '', True)

main()
