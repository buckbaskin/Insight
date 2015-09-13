from flask import render_template
def index():
    vm = {}
    vm['title'] = 'Analytics'
    return render_template('analytics.html',
                           vm=vm)