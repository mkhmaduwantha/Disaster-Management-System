from flask import render_template, request, Blueprint
from emas.models import User

main = Blueprint('main', __name__)


@main.route("/")
def index():
    return render_template('main/home.html')


@main.route("/home")
def home():
    camps = User.query.filter_by(user_type='Camp').all()
    return render_template('main/home_old.html', camps=camps)


@main.route("/about")
def about():
    return render_template('main/about.html', title='About')
