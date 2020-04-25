from flask import render_template, request, Blueprint, flash
from emas.models import User
from emas.main.forms import ContactUs
from emas.users.utils import send_email

main = Blueprint('main', __name__)


@main.route("/", methods=['GET', 'POST'])
def index():
    form = ContactUs()
    if form.validate_on_submit:
        if request.method == 'POST':

            name = form.name.data
            email = form.email.data
            subject = form.subject.data
            message = form.message.data
            # send_email(name=name, email=email,
            # subject=subject, message=message)
            flash(
                f'Thank you for your feedback', 'success')

            form.name.data = ''
            form.email.data = ''
            form.subject.data = ''
            form.message.data = ''
            return render_template('main/index_new.html', form=form)
    # flash(
        # f'Thank you for your feedback', 'success')
    return render_template('main/index_new.html', form=form)


@main.route("/home")
def home():
    camps = User.query.filter_by(user_type='Camp').all()
    return render_template('main/home_old.html', camps=camps)


@main.route("/about")
def about():
    return render_template('main/about.html', title='About')
