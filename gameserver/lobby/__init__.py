from flask import Blueprint
app = Blueprint('lobby', 
	__name__, 
	url_prefix='/', 
	template_folder='templates')
from . import routes