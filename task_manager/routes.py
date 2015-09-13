from flask import render_template, jsonify

def index():
    vm = {}
    vm['title'] = 'Queue Status'
    return render_template('queue.html', 
                           vm=vm)
    
def json():
    return jsonify()