from flask import render_template, request, Blueprint, flash, url_for
from emas.models import User
from emas.main.forms import ContactUs
from emas.users.utils import send_email
import requests
import json
import folium
import pandas as pd
main = Blueprint('main', __name__)


@main.route("/", methods=['GET', 'POST'])
def index():
    form = ContactUs()
    camps = User.query.filter_by(user_type='Camp').all()

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
            return render_template('main/index_new.html', form=form, camps=camps)
    # flash(
        # f'Thank you for your feedback', 'success')

    return render_template('main/index_new.html', form=form, camps=camps)


@main.route("/home")
def home():
    form = ContactUs()
    camps = User.query.filter_by(user_type='Camp').all()

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
            return render_template('main/index_new.html', form=form, camps=camps)
    # flash(
    # f'Thank you for your feedback', 'success')
    return render_template('main/index_new.html', form=form, camps=camps)


@main.route("/about")
def about():
    return render_template('main/about.html', title='About')


@main.route("/disaster")
def disaster():
    data = pd.DataFrame({
        'lat': [79, 80, 81, 82],
        'lon': [5, 6, 7, 8],
        'name': ['Buenos Aires', 'Paris', 'melbourne', 'St Petersbourg'],
        'value': [1, 2, 3, 4]
    })
    data

    # Make an empty map
    m = folium.Map(location=[8, 81], tiles="OpenStreetMap", zoom_start=8)

    # I can add marker one by one on the map
    for i in range(0, len(data)):
        folium.Circle(
            location=[int(data.iloc[i]['lon']), int(data.iloc[i]['lat'])],
            popup=data.iloc[i]['name'],
            radius=int(data.iloc[i]['value']*10),
            color='crimson',
            fill=True,
            fill_color='crimson'
        ).add_to(m)

    # Save it as html
    print('heafag')

    m.save('map.html')
    
    api = requests.get(
        "https://api.covid19api.com/country/sri-lanka/status/confirmed/live")

    print(api.status_code)
    json_data = json.loads(api.text)
    print(api.status_code)
    values = []
    labels = []
    for dic in json_data:
        values.append(dic.get('Cases'))
        labels.append(dic.get('Date'))
    del values[-1]
    del labels[-1]
    legend = 'Monthly Data'

    return render_template('main/disaster_details.html', values=values, labels=labels, legend=legend)
