from flask import render_template, request, Blueprint

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template('main/home.html')
@main.route("/home")
def home():
    
    return render_template('main/home_old.html')


@main.route("/about")
def about():
    return render_template('main/about.html', title='About')

