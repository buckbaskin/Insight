from flask import render_template, jsonify

def index():
    # TODO(buckbaskin):
    vm = {}
    vm['title'] = 'Queue Status'
    return render_template('queue.html', 
                           vm=vm)
    
def json():
    # TODO(buckbaskin):
    return jsonify()