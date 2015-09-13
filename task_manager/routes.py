from flask import render_template, jsonify

def t_index():
    # TODO(buckbaskin):
    vm = {}
    vm['title'] = 'Queue Status'
    return render_template('queue.html', 
                           vm=vm)
    
def t_json():
    # TODO(buckbaskin):
    return jsonify()