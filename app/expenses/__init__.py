from flask import Blueprint

expenses_bp = Blueprint('expenses_bp', __name__,
                        template_folder='templates',
                        url_prefix='/expenses')

from . import views