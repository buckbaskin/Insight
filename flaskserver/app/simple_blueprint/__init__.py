from flask import Blueprint, render_template

simple_page = Blueprint('simple_page', __name__, template_folder='templates', static_folder='static')

print(simple_page.root_path)

@simple_page.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')
