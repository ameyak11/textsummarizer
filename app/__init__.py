from flask import Flask

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#instance of Flask app
app = Flask(__name__)

print "importing webv1 blueprint registered "
from . import webv1 as webv1

app.register_blueprint(webv1.webv1)
print "webV1 blueprint registered"

from . import views
