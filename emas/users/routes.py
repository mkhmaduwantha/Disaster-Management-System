from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from emas import db, bcrypt, admin
from emas.models import User, Role, Message, Address, Notification
from emas.users.forms import (RegistrationForm, LoginForm,
                              RequestResetForm, ResetPasswordForm, MessageForm, UpdateAccountForm, UpdateAccountFormUser, UpdateAccountFormMilitary, UpdateAccountFormCamp)
from emas.users.utils import save_picture, send_reset_email, send_confirmation_email, confirm_token
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from datetime import datetime


users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    # print('hey')
    if current_user.is_authenticated:
        return redirect(url_for('home.home_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # print('hey1.5')
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(title=form.title.data,
                    fname=form.fname.data,
                    lname=form.lname.data,
                    email=form.email.data,
                    mobile_number=form.mobile_number.data,
                    user_type=form.user_type.data,
                    password=hashed_password,
                    )
        # print('hey1')
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        #send_confirmation_email(user)
        # print('hey2')

        flash(
            f'Account created for {form.fname.data}!. A confirmation email has been sent via email.', 'success')
        return redirect(url_for('users.login'))
    return render_template('user/register.html', title='Register', form=form)


@users.route("/confirm_email", methods=['GET', 'POST'])
def request_confirm():
    if current_user.confirmed:
        flash('You have already confirmed your email', 'success')
        return redirect(url_for('users.account'))
    user = User.query.filter_by(email=current_user.email).first()
    send_confirmation_email(user)
    flash('An email has been sent with instructions to rest your password', 'info')
    return redirect(url_for('users.account'))


@users.route('/confirm_email/<token>')
@login_required
def confirm_email(token):
    if current_user.confirmed:
        flash('You have already confirmed your email', 'success')
        return redirect(url_for('users.account'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalidor expired token', 'warning')
        return redirect(url_for('users.account'))
    user.confirmed = True
    db.session.add(user)
    db.session.commit()

    flash('Your email confirmed', 'success')
    return redirect(url_for('users.account'))


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login Successful. Welcome!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home.home_page'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('user/login.html', title='Login', form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.home_page'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    user_confirmed = current_user.confirmed
    form = UpdateAccountForm()
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)

    if form.validate_on_submit():

        if form.picture.data:
            # print('Hey')
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.title = form.title.data
        current_user.fname = form.fname.data
        current_user.email = form.email.data
        current_user.lname = form.lname.data
        current_user.mobile_number = form.mobile_number.data
        current_user.user_type = form.user_type.data
        db.session.commit()
        flash('User information has been updated', 'success')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.title.data = current_user.title
        form.fname.data = current_user.fname
        form.lname.data = current_user.lname
        form.email.data = current_user.email
        form.user_type.data = current_user.user_type
        form.mobile_number.data = current_user.mobile_number
    else:
        flash('User information has not been updated', 'danger')
        return redirect(url_for('users.account'))

    return render_template('user/account.html', title='Account', is_confirmed=user_confirmed, image_file=image_file, form=form,)

   # elif request.method == 'GET':

    #flash('User contact information has been updated', 'success')
    # return redirect(url_for('users.account'))
    # for user in User.query.all():
    #    print (len(user.roles), user.fname)
    #    if len(user.roles) == 1:
    #        print (user.roles[0].name)


@users.route("/contact", methods=['GET', 'POST'])
@login_required
def account_contact():
    user_confirmed = current_user.confirmed
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    user_type = current_user.user_type
    if current_user.user_type == 'None':
        form = UpdateAccountFormUser()
    elif current_user.user_type == 'Military':
        form = UpdateAccountFormMilitary()
    elif current_user.user_type == 'Camp':
        form = UpdateAccountFormCamp()

    if form.validate_on_submit():
        if current_user.user_type == 'None':
            current_user.home_number = form.home_number.data
            home_address = Address(line_one=form.line_one.data,
                                   line_two=form.line_two.data,
                                   city=form.city.data,
                                   district=form.district.data,
                                   province=form.province.data,
                                   postal_code=form.postal_code.data)
            current_user.home_address = []
            current_user.home_address.append(home_address)

        elif current_user.user_type == 'Military':
            current_user.designation = form.designation.data
            current_user.office_number = form.office_number.data
            office_address = Address(line_one=form.line_one.data,
                                     line_two=form.line_two.data,
                                     city=form.city.data,
                                     district=form.district.data,
                                     province=form.province.data,
                                     postal_code=form.postal_code.data)
            current_user.office_address = []
            current_user.office_address.append(office_address)

        elif current_user.user_type == 'Camp':
            current_user.camp_name = form.camp_name.data
            current_user.camp_number = form.camp_number.data
            camp_address = Address(line_one=form.line_one.data,
                                   line_two=form.line_two.data,
                                   city=form.city.data,
                                   district=form.district.data,
                                   province=form.province.data,
                                   postal_code=form.postal_code.data)
            current_user.camp_address = []
            current_user.camp_address.append(camp_address)
            current_user.total_number = form.total_beds.data
            current_user.occupied_number = form.occupied_beds.data
            current_user.remaining_beds = form.remaining_beds.data
            current_user.camp_needs = form.camp_needs.data

        db.session.commit()
        flash('Contact information has been updated', 'success')
        return redirect(url_for('users.account_contact'))

    elif request.method == 'GET':
        if current_user.user_type == 'None':
            if current_user.home_number != None:
                form.home_number.data = current_user.home_number
                form.line_one.data = current_user.home_address[0].line_one
                form.line_two.data = current_user.home_address[0].line_two
                form.district.data = current_user.home_address[0].district
                form.province.data = current_user.home_address[0].province
                form.city.data = current_user.home_address[0].city
                form.postal_code.data = current_user.home_address[0].postal_code
        elif current_user.user_type == 'Military':
            if current_user.office_number != None:
                form.office_number.data = current_user.office_number
                form.designation.data = current_user.designation
                form.line_one.data = current_user.office_address[0].line_one
                form.line_two.data = current_user.office_address[0].line_two
                form.district.data = current_user.office_address[0].district
                form.province.data = current_user.office_address[0].province
                form.city.data = current_user.office_address[0].city
                form.postal_code.data = current_user.office_address[0].postal_code
        elif current_user.user_type == 'Camp':
            if current_user.camp_number != None:
                form.camp_number.data = current_user.camp_number
                form.camp_name.data = current_user.camp_name
                form.camp_needs.data = current_user.camp_needs

                form.total_beds.data = current_user.total_number
                form.occupied_beds.data = current_user.occupied_number
                if current_user.total_number != None:
                    form.remaining_beds.data = int(
                        current_user.total_number.strip()) - int(current_user.occupied_number.strip())
                form.line_one.data = current_user.camp_address[0].line_one
                form.line_two.data = current_user.camp_address[0].line_two
                form.district.data = current_user.camp_address[0].district
                form.province.data = current_user.camp_address[0].province
                form.city.data = current_user.camp_address[0].city
                form.postal_code.data = current_user.camp_address[0].postal_code
    else:
        flash('Contact information has not been updated', 'danger')
        return redirect(url_for('users.account_contact'))

    return render_template('user/contact.html', title='Contact', image_file=image_file, is_confirmed=user_confirmed, form=form, user_type=user_type)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home.home_page'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to rest your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('user/reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home.home_page'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalidor expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to login', 'success')
        return redirect(url_for('users.login'))
    return render_template('user/reset_token.html', title='Reset Password', form=form)


class Controller(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.roles[0].name == 'admin':
                return login.current_user.is_authenticated


admin.add_view(Controller(User, db.session))
admin.add_view(Controller(Role, db.session))


@users.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(email=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        current_user.messages_sent.append(msg)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent.', 'success')
        return redirect(url_for('users.user', email=recipient))
    return render_template('user/send_message.html', title='Send Message',
                           form=form, recipient=recipient, user=user)


@users.route('/user/<email>', methods=['GET', 'POST'])
@login_required
def user(email):
    user = User.query.filter_by(email=email).first_or_404()

    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        current_user.messages_sent.append(msg)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent.', 'success')
        return redirect(url_for('users.user', email=user.email))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user/profile.html', user=user, posts=posts, form=form)


@users.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@users.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    messages = current_user.messages_received
    messages_out = current_user.messages_sent

    return render_template('user/message.html', messages=messages, messages_out=messages_out)


@users.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])
