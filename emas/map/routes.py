from flask import render_template, request, Blueprint
from emas import db
from emas.models import  MapMessage,User
from flask import render_template, url_for, flash, redirect, request, Response, abort
import json
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from flask import app
import math
my_map = Blueprint('my_map', __name__)

def distance(center_lat, center_lng, end_lat, end_lng):
    # convert to radian
    rad_center_lat = math.pi * center_lat / 180
    rad_center_lng = math.pi * center_lng / 180
    rad_end_lat = math.pi * end_lat / 180
    rad_end_lng = math.pi * end_lng / 180

    theta= center_lng-end_lng
    radtheta = math.pi * theta /180
    dist= math.sin(rad_center_lat) * math.sin(rad_end_lat) + math.cos(rad_center_lat) * math.cos(rad_end_lat) * math.cos(radtheta)
    dist= math.acos(dist)
    dist= dist * 180/math.pi
    dist= dist * 60*1.1515
    
    #get in KM
    dist= dist * 1.609344
    return dist

def getrecievers(center_lat, center_lng, end_lat, end_lng, radius, user_id):
    dist=distance(center_lat, center_lng, end_lat, end_lng)
    if(radius<dist):
        return True
    else:
        return False

@my_map.route("/map")
def index():
    return '<p>Hello Map</p>'

@my_map.route("/map/message", methods=['GET','POST'])
def message():
    resp={
    "status":"fail",
    "data":{}
    }
    if request.method == 'POST':
        request_data=request.get_json()

        name=request_data['name']
        message=request_data['message']
        longitude=request_data['longitude']
        lattitude=request_data['lattitude']
        
        try:
            mapMessage = MapMessage(name=name, message=message, longitude=longitude, lattitude= lattitude)
            db.session.add(mapMessage)
            db.session.commit()
            resp={
            "status":"success",
            "data":{ "message sent":'ok'
            }
            }

        except sa.exc.SQLAlchemyError:
            db.session.rollback()
            resp={
            "status":"db_fail",
            "data":{}
            }

    return Response(
            json.dumps(resp),
            mimetype='aplication/json',
            headers={
                'Cache-Control' : 'no-cache',
                'Access-Control-Allow-Origin':'*'
            }
        )

##################################################################################################
#route notifyUser



@my_map.route("/map/notify", methods=['GET','POST'])
def notify():
    resp={
    "status":"fail",
    "data":{}
    }
    
    if request.method == 'POST':
        request_data=request.get_json()

        user_id=request_data['user_id']
        subject=request_data['subject']
        message=request_data['message']
        radius=request_data['radius']
        user_type=request_data['user_type']
        location=request_data['my_location']
        
        print(request_data)
        try:
            mapMessage = MapMessage(name=name, message=message, longitude=longitude, lattitude= lattitude)
            db.session.add(mapMessage)
            db.session.commit()
            resp={
            "status":"success",
            "data":{ "message sent":'ok'
            }
            }

        except sa.exc.SQLAlchemyError:
            db.session.rollback()
            resp={
            "status":"db_fail",
            "data":{}
            }

    return Response(
            json.dumps(resp),
            mimetype='aplication/json',
            headers={
                'Cache-Control' : 'no-cache',
                'Access-Control-Allow-Origin':'*'
            }
        )

@my_map.route('/map/addUserLocation', methods=['GET,POST'])
def addLocation():
    resp={
    "status":"fail",
    "data":{}
    }
    if request.method == 'POST':
        request_data=request.get_json()

        user_id=request_data['user_id']
        lng=request_data['longitude']
        lat=request_data['lattitude']
        
        try:
            UserLocation = UserLocation(user_id=user_id, lng=lng, lat=lat)
            db.session.add(UserLocation)
            db.session.commit()
            resp={
            "status":"success",
            "data":{ "message sent":'ok'
            }
            }

        except sa.exc.SQLAlchemyError:
            db.session.rollback()
            resp={
            "status":"db_fail",
            "data":{}
            }

    return Response(
            json.dumps(resp),
            mimetype='aplication/json',
            headers={
                'Cache-Control' : 'no-cache',
                'Access-Control-Allow-Origin':'*'
            }
        )