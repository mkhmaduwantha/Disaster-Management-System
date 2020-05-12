from flask import render_template, request, Blueprint, flash, url_for, redirect
from emas.models import User
from emas.home.forms import ContactUs
from emas.users.utils import send_email
import requests
import json
import folium
import pandas as pd
home = Blueprint('home', __name__)


@home.route("/", methods=['GET', 'POST'])
@home.route("/home", methods=['GET', 'POST'])
def home_page():
    form = ContactUs()
    camps = User.query.filter_by(user_type='Camp').all()
    is_empty = True
    if len(camps) != 0:
        is_empty = False

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
            return rediretc('home.home_page')
    # flash(
    # f'Thank you for your feedback', 'success')
    return render_template('home/home.html', form=form, camps=camps, is_true=True, is_empty=is_empty)


@home.route("/about")
def about():
    return render_template('home/about.html', title='About')


@home.route("/disaster/<name>")
def disaster(name):
    if name == 'covid':
        data = pd.DataFrame({
            'lat': [79.8612, 79.9607, 80.0098, 79.8394, 80.3609],
            'lon': [6.9271, 6.5854, 7.0840, 8.0408, 7.4818],
            'name': ['Colombo', 'Kaluthara', 'Gampaha', 'Puttlam', 'Kurrunegala'],
            'value': [160, 65, 53, 41, 27]
        })

        data
        m = folium.Map(width=700, height=1000, location=[8, 81], tiles="OpenStreetMap", zoom_start=8, zoom_control=False,
                       scrollWheelZoom=False,
                       dragging=False)
        for i in range(0, len(data)):
            folium.Circle(
                location=[data.iloc[i]['lon'], data.iloc[i]['lat']],
                popup=data.iloc[i]['name'] + '\n' + str(data.iloc[i]['value']),
                radius=int(data.iloc[i]['value']*100),
                color='crimson',
                fill=True,
                fill_color='crimson'
            ).add_to(m)
        html = m.get_root().render()
        api = requests.get(
            "https://api.covid19api.com/country/sri-lanka/status/confirmed/live")

        print(api.status_code)
        json_data = json.loads(api.text)
        values = []
        labels = []
        for dic in json_data:
            values.append(dic.get('Cases'))
            labels.append(dic.get('Date'))
        labels_split = []
        for label in labels:
            label_temp = label.split('T')[0]
            labels_split.append(label_temp)
        legend = ' Number of confirmed Cases in Sri Lanka'
        details = 'COVID-19, an infectious disease caused by a new strain of the coronavirus, is quickly making its way around the world, making everyone wonder what they can do to aid in coronavirus prevention and ensuring they and others don’t contract this contagious disease.'
        reference = 'https://visme.co/blog/coronavirus-prevention/'
        dos = ['Wash your hands frequently for 20+ seconds with soap and water',
               'Stay at home and limit contact with others',
               'Routinely clean frequently touched spaces in your home',
               'Seek medical help if you’re suffering from a fever, cough or difficulty breathing',
               'Limit contact with pets and animals']
        donts = ['Don’t go to crowded areas',
                 'Don’t touch your face',
                 'Don’t be in close contact with others',
                 'Don’t ignore symptoms',
                 'Don’t leave your home, especially if sick']
        image_file_1 = url_for(
            'static', filename='disaster_pics/' + name + '_1.jpg')
        image_files = [image_file_1, image_file_1, image_file_1]
    return render_template('home/disaster_details.html', values=values, labels=labels_split, legend=legend, details=details, reference=reference, dos=dos, donts=donts, html=html, image_files=image_files)


@home.route("/getmap")
def getmap():
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

    return render_template('home/map.html', html=m.get_root().render())
