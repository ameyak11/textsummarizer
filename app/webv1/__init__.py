from flask import Blueprint
print "creating blueprint"
webv1 = Blueprint('webv1', __name__, url_prefix='/web/v1')

from . import controllers