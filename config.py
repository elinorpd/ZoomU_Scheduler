import os

DEBUG=True

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'elinor'

base = os.path.abspath(os.path.dirname(__file__))