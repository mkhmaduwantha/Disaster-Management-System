from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
from flask_login import login_user, current_user, logout_user, login_required
from emas import db, bcrypt, admin
from emas.models import User, Role, Message, EUser
from emas.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm, MessageForm)
from emas.users.utils import save_picture, send_reset_email, send_confirmation_email, confirm_token
from flask_admin.contrib.sqla import ModelView 
from flask_admin import AdminIndexView, expose
from datetime import datetime




users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    print ('hey')
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        print ('hey1.5')
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  
        user = EUser(title=form.title.data, 
                    fname=form.fname.data, 
                    lname=form.lname.data, 
                    email=form.email.data, 
                    mobile_number=form.mobile_number.data,
                    user_type = form.user_type.data,
                    password = hashed_password)
        print ('hey1')
        db.session.add(user)
        db.session.commit()
        print ('hey2')

        flash(f'Account created for {form.fname.data}!. A confirmation email has been sent via email.', 'success')
        return redirect(url_for('users.login'))
    return render_template('user/register.html', title='Register', form=form)

@users.route("/confirm_email", methods = ['GET','POST'])
def request_confirm():
    if current_user.confirmed:
        flash('You have already confirmed your email', 'success')
        return redirect(url_for('users.account'))    
    user = User.query.filter_by(email = current_user.email).first()
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

    flash('Your email confirmed','success')
    return redirect(url_for('users.account'))


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('user/login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    user_confirmed = current_user.confirmed
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.fname = form.fname.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.fname.data = current_user.fname
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    for user in User.query.all():
        print (len(user.roles), user.fname)
        if len(user.roles) == 1:
            print (user.roles[0].name)
    return render_template('user/account.html', title='Account', is_confirmed = user_confirmed, image_file = image_file, form = form)


@users.route("/reset_password", methods = ['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))    
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to rest your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('user/reset_request.html', title = 'Reset Password', form = form)

@users.route("/reset_password/<token>", methods = ['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home')) 
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalidor expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')     
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to login','success')
        return redirect(url_for('users.login'))
    return render_template('user/reset_token.html', title = 'Reset Password', form = form)   




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
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent.','success')
        return redirect(url_for('main.home', username=recipient))
    return render_template('user/send_message.html', title='Send Message',
                           form=form, recipient=recipient)



@users.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user/profile.html', user=user, posts=posts)

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

    return render_template('user/messages.html', messages=messages)

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