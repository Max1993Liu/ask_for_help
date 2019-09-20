import smtplib
import ssl
import json
import os
import functools
from pathlib import Path
from email.message import EmailMessage

# from .trackerror import get_code


__all__ = ['ask_for_help', 'show_recipients', 'add_recipient', 'reset_my_email']



_CONFIG_PATH = Path(__file__).absolute().parent / 'config.json'


def get_config():
	with open(_CONFIG_PATH, 'rb') as f:
		return json.load(f)


def write_config(config):
	with open(_CONFIG_PATH, 'wb') as f:
		return json.dump(config, f)


def add_recipient(name, email):
	config = get_config()['GOOD_PEOPLE']
	if name in config['GOOD_PEOPLE']:
		raise ValueError('{} is already in your recipient list.'.format(name))
	config['GOOD_PEOPLE'][name] = email
	write_config(config)


def show_recipients():
	return get_config()['GOOD_PEOPLE']


def reset_my_email(email):
	config = get_config()
	addr = input('Enter your email address:')
	pwd = input('Enter your email password:')
	config['MY_EMAIL'] = addr
	config['MY_PASSWORD'] = pwd
	write_config(config)


def init_setting():
	config = get_config()
	if config['MY_EMAIL'] == 'x@x.com':
		addr = input('Enter your email address:')
		pwd = input('Enter your email password:')
		config['MY_EMAIL'] = addr
		config['MY_PASSWORD'] = pwd
	write_config(config)


def send_email(msg, address):
	""" Send msg to Max """
	context = ssl.create_default_context()
	
	with smtplib.SMTP_SSL("smtp.exmail.qq.com", 465, context=context) as server:
		MY_EMAIL, MY_PASSWORD = get_config['MY_EMAIL'], get_config['MY_PASSWORD']
		server.login(MY_EMAIL, MY_PASSWORD)
		server.send_message(msg, MY_EMAIL, [address])
		server.close()    


def create_message(code, ex_msg, address):
	""" Create an error report"""
	msg = EmailMessage()
	content = 'Error Message:\n' + ex_msg + '\n\nSource Code:\n' + code
	msg.set_content(content.replace('\t', ' '*4))  # replace tab with spaces for better formatting

	MY_EMAIL = get_config()['MY_EMAIL']
	msg['Subject'] = '{} needs your help!'.format(MY_EMAIL.split('@')[0])
	msg['From'] = MY_EMAIL
	msg['To'] = address
	return msg



class ask_for_help:

	def __init__(self, who=None):
		init_setting()

		recipients = get_config()['GOOD_PEOPLE']
		available = list(recipients.keys())
		
		if who and who not in available:
			raise ValueError('Please add {} to the recipients list using add_recipient.'.format(who))
	
		if who is None:
			who = available[0]
		
		self.who = who
		self.address = recipients[who]

	def __call__(self, f):
		f_name = f.__name__

		@functools.wraps(f)
		def wrapped(*args, **kwargs):
			try:
				return f(*args, **kwargs)
			except Exception as e:
				# generate an error report
				source_code = get_code(f)
				ex_msg = str(e)

				error_report = create_message(source_code, ex_msg, self.address)
				send_email(error_report, self.address)
				print('{} will help you!'.format(self.who))
		return wrapped
