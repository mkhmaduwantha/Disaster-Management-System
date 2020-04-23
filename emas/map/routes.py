from flask import render_template, request, Blueprint
from emas import db
from emas.models import  MapMessage
from flask import render_template, url_for, flash, redirect, request, Response, abort
import json


my_map = Blueprint('my_map', __name__)

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
            "data":{
            }
            }

        except exec.SQLAlchemyError:
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

