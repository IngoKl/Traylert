from infi.systray import SysTrayIcon
from traylert.traylert_crypto import encrypt, decrypt
from win10toast import ToastNotifier
import click
import configparser
import json
import jsonpickle
import requests
import time
import os
from pathlib import Path


def fetch_system_info(config, endpoint_override=False):
	if not endpoint_override:
		r = requests.get(config['CLIENT']['endpoint'])
	else:
		r = requests.get(endpoint_override)

	if not config['CRYPTO'].getboolean('aes'):
		return r.text
	else:
		system_info_json = decrypt(jsonpickle.decode(r.text), config['CRYPTO']['encryption_key'])
		return json.loads(system_info_json)


def do_nothing(sysTrayIcon):
	pass


@click.command()
@click.option('--config_file', default=False, help='A configuration .ini')
@click.option('--endpoint_override', default='http://127.0.0.1:5000', help='The endpoint to connect to.')
def main(endpoint_override=False, config_file=False):

	# Icon
	if os.path.dirname(__file__) is not '':
		icon = os.path.dirname(__file__) + '/../data/traylert.ico'
	else:
		icon = '../data/traylert.ico'

	# Config
	config = configparser.ConfigParser()

	if not config_file:
		if os.path.dirname(__file__) is not '':
			config.read(os.path.dirname(__file__) + '/traylert.ini')
		else:
			config.read('traylert.ini')
	else:
		config.read(config_file)

	toaster = ToastNotifier()
	systray = SysTrayIcon(icon, 'Traylert', None)
	systray.start()

	alerts = [('None', 'None')]

	while True:
		if not endpoint_override:
			system_info = fetch_system_info(config)
		else:
			system_info = fetch_system_info(config, endpoint_override)

		if system_info['alerts'] != alerts:
			if len(system_info['alerts']) > 0:
				for alert in system_info['alerts']:
					toaster.show_toast('Traylert', f'{alert[0]}\n{alert[1]}')
				alerts = system_info['alerts']


		menu_options = []
		for key, value in system_info.items():
			if type(value) != list:
				menu_options.append((f'{key} - {value}', None, do_nothing))

		systray.shutdown()
		systray = SysTrayIcon(icon, f'Last Alert: {alerts[-1]}',  tuple(menu_options))
		systray.start()

		time.sleep(config.getint('CLIENT', 'refresh_time'))


if __name__ == '__main__':
	main()