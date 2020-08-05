from . import app
from flask import redirect,url_for
from flask import jsonify, request

@app.route('/')
def index():
    #return jsonify("WEB DEMO working")
    return redirect(url_for('webv1.show_demo'))
