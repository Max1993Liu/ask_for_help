import smtplib
import ssl
import functools
from email.message import EmailMessage

from .config import *
from .trackerror import get_code


def send_email(msg, address):
	""" Send msg to Max """
	context = ssl.create_default_context()
	
	with smtplib.SMTP_SSL("smtp.exmail.qq.com", 465, context=context) as server:
		server.login(MY_EMAIL, MY_PASSWORD)
		server.send_message(msg, MY_EMAIL, [address])
		server.close()    


def create_message(code, ex_msg, address):
	""" Create an error report"""
	msg = EmailMessage()
	content = 'Error Message:\n' + ex_msg + '\n\nSource Code:\n' + code
	msg.set_content(content.replace('\t', ' '*4))  # replace tab with spaces for better formatting

	msg['Subject'] = '{} needs your help!'.format(MY_EMAIL.split('@')[0])
	msg['From'] = MY_EMAIL
	msg['To'] = address
	return msg


class ask_for_help:

	def __init__(self, who=None):
		available = list(GOOD_PEOPLE.keys())
		
		if who and who not in available:
			raise ValueError('Please add {} to the GOOD_PEOPLE list in the config file.'.format(who))
	
		if who is None:
			who = available[0]
		
		self.who = who
		self.address = GOOD_PEOPLE[who]

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
