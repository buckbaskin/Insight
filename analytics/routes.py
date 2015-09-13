from flask import render_template
from flask import jsonify
def a_index():
    vm = {}
    vm['title'] = 'Analytics'
    return render_template('analytics.html',
                           vm=vm)
    
def a_json():
    return jsonify()