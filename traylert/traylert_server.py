from collections import deque
from flask import Flask, make_response, request, abort
from traylert.traylert_crypto import encrypt, decrypt
import configparser
import datetime
import json
import jsonpickle
import os
import psutil
import shutil


config = configparser.ConfigParser()

if os.path.dirname(__file__) is not '':
	config.read(os.path.dirname(__file__) + '/traylert.ini')
else:
	config.read('traylert.ini')

app = Flask(__name__)

alerts = deque(maxlen=config.getint('ALERTS', 'alert_queue_length'))


def set_alert(datetime, alert):
	alerts.append((datetime.strftime('%Y-%m-%d %H:%M:%S'), alert))


def get_system_info():
	# disc space
	total, used, free = shutil.disk_usage(config['SERVER']['monitored_disc'])

	# disc space is converted to GB
	sys = {'discspace_free (GB)': f'{round(free / float(1<<30), 2)} ({round(free/used*100)}%)', 
	       'memory': f'{psutil.virtual_memory()[2]} %',
	       'alerts': tuple(alerts)}


	# disc space alert
	if free/used < config.getfloat('ALERTS', 'threshold_min_disc_space'):
		set_alert(datetime.datetime.now(), 'Disc space is running low!')


	return json.dumps(sys, ensure_ascii=False)


@app.route('/alert', methods=['POST'])
def alert():
		if request.remote_addr in config['ALERTS']['alert_ips_whitelist']:
			set_alert(datetime.datetime.now(), request.form['alert'])
			return make_response('', 200)
		else:
			abort(401)


@app.route('/')
def information():
	if not config['CRYPTO'].getboolean('aes'):
		return get_system_info()
	else:
		encrypted = encrypt(get_system_info(), config['CRYPTO']['encryption_key'])
		return jsonpickle.encode(encrypted)


if __name__ == "__main__":
    app.run()