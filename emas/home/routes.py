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
        title = "Covid-19"
        dtype = "Man-made"
        subtitle1 = "Do's"
        subtitle2 = "Dont's"
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

        return render_template('home/disaster_details.html', values=values, labels=labels_split, legend=legend, details=details, reference=reference, dos=dos, donts=donts, html=html, image_files=image_files, type=dtype, title=title, subtitle1=subtitle1, subtitle2=subtitle2)
    elif name == 'bomb-blasts':
        title = "Bomb Blasts"
        dtype = "Man-made"
        subtitle1 = "Detection and avoiding"
        subtitle2 = "Effects"
        data = pd.DataFrame({
            'lat': [79.8612,  80.6337, 81.6747, 81.2152],
            'lon': [6.9271, 7.2906,  7.7310, 8.5874],
            'name': ['Colombo', 'Kandy', 'Batticalo', 'Trincomalee'],
            'value': [10, 1, 2, 4]
        })

        data
        m = folium.Map(width=700, height=1000, location=[8, 81], tiles="OpenStreetMap", zoom_start=8, zoom_control=False,
                       scrollWheelZoom=False,
                       dragging=False)
        for i in range(0, len(data)):
            folium.Circle(
                location=[data.iloc[i]['lon'], data.iloc[i]['lat']],
                popup=data.iloc[i]['name'] + '\n' + str(data.iloc[i]['value']),
                radius=int(data.iloc[i]['value']*3000),
                color='crimson',
                fill=True,
                fill_color='crimson'
            ).add_to(m)
        html = m.get_root().render()

        values = [774, 207, 6, 0, 0, 0, 0, 0, 0, 250]
        labels = [1990, 1996, 2006, 2009, 2010, 2012, 2014, 2016, 2018, 2019]
        labels_split = labels
        legend = ' Number of Deaths - Sri Lanka'
        details = 'The most serious manmade disaster, a threat to detonate an explosive or incendiary device to cause property damage, death, or injuries, whether or not such a device actually exists'
        reference = 'science.howstuffworks.com/blast-resistant..'
        dos = ['Explosive detector:detect bombs, find mere traces of explosives',
               'xray inspection machine, detector, walk-through weapon detector are very sensitive to the bombs.',
               'be calm',
               'crawl under a sturdy table or a solid object and remain there for at least one minute',
               'leave the building and go as much as far away as soon as possible',
               'don’t use elevators',
               'dig a hole or find a place below ground level and hide there',
               'Hiroshima and Nagasaki bomb blast: death toll between 129, 000 - 240, 000',
               'Deaths(burns, radiation, cancer)',
               'leukemia, thyroid cancer, lung cancer(3800) and breast cancer',
               'newly born babies abnormal and most died',
               'land become without nutrients and cities, buildings destroyed taking back success.'
               ]
        donts = ['Sri Lanka last 2019 April 21',
                 'Easter Sunday',
                 'Churches, luxury hotels in Colombo, housing complex in Dematagoda, a guest house in Dehiwala',
                 '259 deaths 45, foreign nationals, 3 police officers, 500 injured'
                 ]
        image_file_1 = url_for(
            'static', filename='disaster_pics/' + name + '_1.jpg')
        image_files = [image_file_1, image_file_1, image_file_1]
        return render_template('home/disaster_details.html', values=values, labels=labels_split, legend=legend, details=details, reference=reference, dos=dos, donts=donts, html=html, image_files=image_files, type=dtype, title=title, subtitle1=subtitle1, subtitle2=subtitle2)
    elif name == 'bio-weapons':
        title = "Bio Weapons"
        dtype = "Man-made"
        subtitle1 = "Detection and avoiding"
        subtitle2 = "Effects"
        data = pd.DataFrame({
            'lat': [5.4673,  95.7129, 37.9062, 105.3188, 138.2529],
            'lon': [57.8868, 37.0902, 0.0236, 61.5240, 36.2048],
            'name': ['Gruinard', 'US', 'Kenya', 'Russia', 'Japan'],
            'value': [10, 20, 30, 40, 50]
        })

        data
        m = folium.Map(width=1450, height=700, location=[8, 81], tiles="OpenStreetMap", zoom_start=2, zoom_control=False,
                       scrollWheelZoom=False,
                       dragging=False)
        for i in range(0, len(data)):
            folium.Circle(
                location=[data.iloc[i]['lon'], data.iloc[i]['lat']],
                popup=data.iloc[i]['name'] + '\n' + str(data.iloc[i]['value']),
                radius=int(data.iloc[i]['value']*5000),
                color='crimson',
                fill=True,
                fill_color='crimson'
            ).add_to(m)
        html = m.get_root().render()

        values = []
        labels = []
        labels_split = labels
        legend = ' Number of incidents in Sri Lanka'
        details = '''Biological weapons are microorganisms like virus, bacteria, fungi, or other toxins that are produced and released deliberately to cause disease and death in humans, animals or plants. 
                     Biological agents, like anthrax, botulinum toxin and plague can pose a difficult public health challenge causing large numbers of deaths in a short amount of time while being difficult to contain. Bioterrorism attacks could also result in an epidemic, for example if Ebola or Lassa viruses were used as the biological agents. '''
        reference = 'science.howstuffworks.com/blast-resistant..'
        dos = ['Dont count on a vaccine being available',
               'Stay informed',
               'Get your yearly flu vaccine shot.',
               'Get a pneumonia vaccine shot',
               'Use anti-viral medications if advised to do so by a health professional or by the government',
               'Wash your hands frequently',
               'Use an alcohol-based disinfectant',
               'Avoid exposure to infected'

               ]
        donts = ['600 bc	Solon uses the purgative herb hellebore during the siege of Krissa',
                 '1155	Emperor Barbarossa poisons water wells with human bodies in Tortona, Italy',
                 '1346	Tartar forces catapult bodies of plague victims over the city walls of Caffa, Crimean Peninsula(now Feodosia, Ukraine)',
                 '1495	Spanish mix wine with blood of leprosy patients to sell to their French foes in Naples, Italy',
                 '1675	German and French forces agree to not use “poisones bullets”',
                 '1710	Russian troops catapult human bodies of plague victims into Swedish cities',
                 '1763	British distribute blankets from smallpox patients to Native Americans',
                 '1797	Napoleon floods the plains around Mantua, Italy, to enhance the spread of malaria',
                 '1863	Confederates sell clothing from yellow fever and smallpox patients to Union troops during the US Civil War',
                 'World War I	German and French agents use glanders and anthrax',
                 'World War II	Japan uses plague, anthrax, and other diseases',
                 'several other countries experiment with and develop biological weapons programs',
                 '1980–1988	Iraq uses mustard gas, sarin, and tabun against Iran and ethnic groups inside Iraq during the Persian Gulf War',
                 '1995	Aum Shinrikyo uses sarin gas in the Tokyo subway system'
                 ]
        image_file_1 = url_for(
            'static', filename='disaster_pics/' + name + '_1.jpg')
        image_files = [image_file_1, image_file_1, image_file_1]
        return render_template('home/disaster_details.html', values=values, labels="none", legend=legend, details=details, reference=reference, dos=dos, donts=donts, html=html, image_files=image_files, type=dtype, title=title, subtitle1=subtitle1, subtitle2=subtitle2)

    elif name == 'tsunami':
        title = "Tsunami"
        dtype = "Natural"
        subtitle1 = "Before and After"
        subtitle2 = "Effects"
        data = pd.DataFrame({
            'lat': [79.8612, 79.9607, 80.2210,  80.5550, 81.1212, 81.6747, 81.2152, 80.8142, 80.0255, 80.3770, 79.9044, 79.8394],
            'lon': [6.9271, 6.5854, 6.0535, 5.9549, 6.1429, 7.7310, 8.5874, 9.2671, 9.6615, 9.3803, 8.9810, 8.0408],
            'name': ['Colombo', 'Kaluthara', 'Galle', 'Mathara', 'Hambanthota', 'Batticalo', 'Trincomalee', 'Mulativ', 'Jaffna',  'Kilinochchi', 'Mannar', 'Puttlam'],
            'value': [80, 80, 100, 100, 100, 150, 150, 100, 100, 80, 80, 80]
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

        values = [1, 2, 5, 8, 4, 7, 9, 5, 6, 10,
                  14, 15, 14, 16, 18, 22, 25, 21, 19, 24]
        labels = [int(x) for x in range(2001, 2021)]
        labels_split = labels
        legend = ' Number of Incidents by Year - worldwide'
        details = 'A series of ocean waves sends surges widespread destruction when they crash ashore caused by large, undersea earthquakes at tectonic plate boundaries'
        reference = 'en.wikinews.org/wiki/Tsunami_death_toll_updated'
        dos = ['Important to have a well-made plan in advance',
               'Better to choose a safe location not more than 2 miles away from the coastal area or that is 100 feet above the sea level',
               'The safety area should be reached in 15 minutes, by walking on foot and not by a vehicle',
               'After an earthquake, it’s better to listen to what the authorities have to say',
               'Having multiple choices of safety routes is very much important',
               'As soon as hearing a tsunami warning, leaving the current location immediately and head towards the safety area',
               'Not good to watch the waves from high cliffs, stand close to bridges and rivers, and stay at any fallen power lines',
               'Better to avoid living in coastal areas',
               'Elevating the houses level in coastal area',
               'Inviting an expert to take a look at the location and check for any weak spots or advising'
               ]
        donts = ['Indian Ocean tsunami disaster: 126, 473 dead and 93, 943 missing in Indonesia',
                 'Northern tip of Sumatra(in Indonesia) on December 26 in 2014',
                 'In Sri Lanka, 30957 dead, 5637 missing',
                 'Total dead and missing for all eleven countries damaged by the tsunami now stands at 282, 517',
                 ]
        image_file_1 = url_for(
            'static', filename='disaster_pics/' + name + '_1.jpg')
        image_files = [image_file_1, image_file_1, image_file_1]
        return render_template('home/disaster_details.html', values=values, labels=labels_split, legend=legend, details=details, reference=reference, dos=dos, donts=donts, html=html, image_files=image_files, type=dtype, title=title, subtitle1=subtitle1, subtitle2=subtitle2)

    elif name == 'floods':
        title = "Floods"
        dtype = "Natural"
        subtitle1 = "Effects"
        subtitle2 = "Results"
        data = pd.DataFrame({
            'lat': [79.8612, 79.9607, 80.2210,  80.5550, 81.1212, 81.6747, 81.2152, 80.8142, 80.4982, 80.6337, 80.6234, 80.3464, 80.3847,  80.7891],
            'lon': [6.9271, 6.5854, 6.0535, 5.9549, 6.1429, 7.7310, 8.5874, 9.2671, 8.7542, 7.2906, 7.4675, 7.2513, 6.7056, 6.9497],
            'name': ['Colombo', 'Kaluthara', 'Galle', 'Mathara', 'Hambanthota', 'Batticalo', 'Trincomalee', 'Mulativ', 'Vavuniya',  'Kandy', 'Matale', 'Kegalle', 'Ratnapura', 'Nuwara Eliya'],
            'value': [201.72, 1079.06, 1513.6, 1317.7, 103.68, 0.2, 6.96, 0.72, 1.02, 110.2, 0.4, 0.31, 57, 693]
        })

        data
        m = folium.Map(width=700, height=1000, location=[8, 81], tiles="OpenStreetMap", zoom_start=8, zoom_control=False,
                       scrollWheelZoom=False,
                       dragging=False)
        for i in range(0, len(data)):
            folium.Circle(
                location=[data.iloc[i]['lon'], data.iloc[i]['lat']],
                popup=data.iloc[i]['name'] + '\n' +
                str(data.iloc[i]['value']),
                radius=int(data.iloc[i]['value']*20),
                color='crimson',
                fill=True,
                fill_color='crimson'
            ).add_to(m)
        html = m.get_root().render()

        values = [280000, 90000, 210000, 733479, 340068, 415471, 605903, 499887,
                  1262506, 453429, 453429, 2524402, 536318, 1100000, 240000, 350000, 65000, 180000]
        labels = [int(x) for x in range(2003, 2019)]
        labels_split = labels
        legend = ' Number of affected by Year - Sri Lanka'
        details = '''When water inundates land that's normally dry
                     floodplain: the place where there is excessive rain, a ruptured dam or levee, rapid melting of snow or ice, or even an unfortunately placed beaver dam can overwhelm a river, spreading over the adjacent land.
                     Whenever a large storm or tsunami causes the sea to surge inland
                     Most take days to develop, others generate quickly and with little warning.
                     Extreme weather events and rising seas(melting glaciers), climate change is increasing the risk of floods worldwide, coastal and low-lying areas
                     Governments mandate residents of flood-prone locations purchase flood insurance, set construction  requirements aimed at making buildings more flooded resistant - with varying degrees of success.'''

        reference = 'www.nationalgeographic.com/.../floods'
        dos = ['Decrease the level of social, economic and environmental sites',
               'The amount of damage depends on the location, extent of flooding, the vulnerability, value of the natural and constructed environments, and duration, depth and speed',
               'Loss of human life, damage to property, destruction of crops, loss of livestock, deterioration of health conditions'
               ]
        donts = ['In 2017 : Southwest monsoon period(late May to the beginning of June)',
                 'Kukuleganga, Galle, Ratnapura, Kegalle, Kalutara, Matara, Hambantota, Nuwara Eliya',
                 'Death toll 45 school children',
                 '95 missing',
                 '77, 000 people were evacuated from the floods and relocated to safe locations',
                 'Sixteen hospitals in the flood-affected areas were also evacuated'
                 ]
        image_file_1 = url_for(
            'static', filename='disaster_pics/' + name + '_1.jpg')
        image_files = [image_file_1, image_file_1, image_file_1]
        return render_template('home/disaster_details.html', values=values, labels=labels_split, legend=legend, details=details, reference=reference, dos=dos, donts=donts, html=html, image_files=image_files, type=dtype, title=title, subtitle1=subtitle1, subtitle2=subtitle2)

    elif name == 'landslides':
        title = "Landslides"
        dtype = "Natural"
        subtitle1 = "Before"
        subtitle2 = "effects"
        data = pd.DataFrame({
            'lat': [79.8612, 79.9607, 80.2210,  80.5550, 81.1212,   80.6337, 80.6234, 80.3464, 80.3847,  80.7891],
            'lon': [6.9271, 6.5854, 6.0535, 5.9549, 6.1429,   7.2906, 7.4675, 7.2513, 6.7056, 6.9497],
            'name': ['Colombo', 'Kaluthara', 'Galle', 'Mathara', 'Hambanthota',   'Kandy', 'Matale', 'Kegalle', 'Ratnapura', 'Nuwara Eliya'],
            'value': [8, 45, 25, 30, 8, 70, 40, 78, 100, 200]
        })

        data
        m = folium.Map(width=700, height=1000, location=[8, 81], tiles="OpenStreetMap", zoom_start=8, zoom_control=False,
                       scrollWheelZoom=False,
                       dragging=False)
        for i in range(0, len(data)):
            folium.Circle(
                location=[data.iloc[i]['lon'], data.iloc[i]['lat']],
                popup=data.iloc[i]['name'] + '\n' +
                str(data.iloc[i]['value']),
                radius=int(data.iloc[i]['value']*100),
                color='crimson',
                fill=True,
                fill_color='crimson'
            ).add_to(m)
        html = m.get_root().render()

        values = [10, 12, 84, 1, 20, 10, 35, 5,
                  25, 3, 2, 20, 80, 45, 48, 370, 280, 80]
        labels = [int(x) for x in range(1974, 2010, 2)]
        labels_split = labels
        legend = 'Number of Incidents by Year - Sri Lanka'
        details = '''Movement of a mass of rock, debris, or earth down a slope
                Heavy rain, flooding, earthquakes, volcanoes, fires and even irresponsible development of land
                can be initiated in slopes already on the verge of movement by rainfall, snowmelt, changes in water level, stream erosion, changes in ground water, earthquakes, volcanic activity, disturbance by human activities, or any combination of these factors.
                If trees, electric or telephone poles are sloping in a similar direction or appear to be uneven, there is a chance that the ground underneath may be unstable
                Hilly retain areas are special
                Any area that is on a slope or beneath elevated terrain'''

        reference = 'www.usgs.gov/faqs/what-a-landslide-and-what..'
        dos = ['Identifying risk areas and avoiding them',
               'If one is approaching,  get to either side of the moving ground',
               'If  get caught in the path, curl yourself up in a ball',
               'appearance of unstable ground'
               ]
        donts = ['last:2017 in Sri Lanka',
                 'landslides and floods in Sri Lanka have killed at least 151 people',
                 'More than 100 still missing after the worst rains in the Indian Ocean island since 2003',
                 'death toll 151, 111 missing and 95 injured',
                 '500, 000 affected'
                 ]
        image_file_1 = url_for(
            'static', filename='disaster_pics/' + name + '_1.jpg')
        image_files = [image_file_1, image_file_1, image_file_1]
        return render_template('home/disaster_details.html', values=values, labels=labels_split, legend=legend, details=details, reference=reference, dos=dos, donts=donts, html=html, image_files=image_files, type=dtype, title=title, subtitle1=subtitle1, subtitle2=subtitle2)


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

    return render_template('http://lcoalhost:3000/Chat')
