from flask import render_template, request, Blueprint
from emas import db
from emas.models import  MapMessage,User,Marker
from flask import render_template, url_for, flash, redirect, request, Response, abort
import json
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from flask import app
import math
import emas.map.MyMap as MapFunctions
from flask_cors import CORS
import emas.map.MyMap

my_map = Blueprint('my_map', __name__)
CORS(my_map)


@my_map.route("/map")
def index():
    return '<p>Hello Map</p>'

@my_map.route('/map/addMarker', methods=['GET','POST'])
def addMarker():
    resp={'query':''}
    if request.method == 'POST':
        request_data=request.get_json()

        user_id=request_data['user_id']
        lng=request_data['lng']
        lat=request_data['lat']
        mtype=request_data['mtype']
        subject=request_data['subject']
        color=request_data['color']
        name=request_data['name']
        radius=request_data['radius']
        description=request_data['description']
        address=request_data['address']
        
        try:
                marker1=Marker(lng=lng,lat=lat,color=color,name=name,type=mtype,radius=radius,subject=subject,description=description,address=address,user_id=user_id)
                db.session.add(marker1)
                db.session.commit()
                resp={'query':'ok'} 

        except sa.exc.SQLAlchemyError:
                db.session.rollback()
                
                resp={'not_ok': str(sa.exc.IntegrityError) }
        finally:
                db.session.close()
    return Response(
         json.dumps(resp)
    )

@my_map.route('/map/getMarkers', methods=['GET','POST'])
def getMarkers():
    resp={'query':''}
    if request.method == 'POST':
        try:
                r=db.engine.execute('select * from marker')
                tempList=[]
                perList=[]
                for i in r:
                    time=float(i[10].split()[1][0:5].split(':')[0])
                    if time<12:
                        time=i[10].split()[1][0:5]+'am'
                    else:
                        time=i[10].split()[1][0:5]+'pm'
                    if i[5]=='permanant':
                        perList.append({'marker_id':i[0],
                                'lng':i[1],
                                'lat':i[2],
                                'color':i[3],
                                'name':i[4],
                                'mtype':i[5],
                                'radius':i[6],
                                'subject':i[7],
                                'description':i[8],
                                'address':i[9].split(','),
                                'date':i[10].split()[0],
                                'time':time,
                                'user_id':i[11]
                                })
                    else:
                        tempList.append({'marker_id':i[0],
                                'lng':i[1],
                                'lat':i[2],
                                'color':i[3],
                                'name':i[4],
                                'mtype':i[5],
                                'radius':i[6],
                                'subject':i[7],
                                'description':i[8],
                                'address':i[9].split(','),
                                'date':i[10].split()[0],
                                'time':i[10].split()[1][0:5],
                                'user_id':i[11]
                                })
                resp={'query':'ok',
                        'data': {
                            "permanantList":list(perList),
                            "tempList":list(tempList)
                            }} 

        except sa.exc.SQLAlchemyError:
                db.session.rollback()
                
                resp={'query':'not_ok' }
        finally:
                db.session.close()
    return Response(
         json.dumps(resp)
    )

@my_map.route('/map/getMarkerDetail', methods=['GET','POST'])
def getMarkerDetails():
    resp={'query':''}
    if request.method == 'POST':
        id = request.args.get('id')
        try:
                marker = Marker.query.filter_by(id=id).first()
                detailList=[]
                if marker:
                    detailList.append(
                                    marker)
                    resp={'query':'ok',
                            'data': {
                                "mDetailLList":list(detailList)
                                }} 
                else:
                     resp={'query':'not_ok' }

        except sa.exc.SQLAlchemyError:
                db.session.rollback()
                
                resp={'query':'not_ok' }
        finally:
                db.session.close()
    return Response(
         json.dumps(resp)
    )

@my_map.route('/map/delMarker', methods=['GET'])
def delMarker():
    resp={'query':''}
    if request.method == 'GET':
        id = int(request.args.get('id'))
        try:
            marker = Marker.query.filter_by(id=id).first()
            db.session.delete(marker)
            db.session.commit()
            resp={'query':'ok' }
        except sa.exc.SQLAlchemyError:
            db.session.rollback()    
            resp={'query':'not_ok' }
        finally:
                db.session.close()
    return Response(
        json.dumps(resp)
    )

@my_map.route('/map/getMyMarker', methods=['GET'])
def getMyMarker():
    resp={'query':''}
    if request.method == 'GET':
        id = request.args.get('id')
        try:
            r=db.engine.execute('select * from marker where user_id='+str(id))
            dList=[]
            for i in r:
                if float(i[10].split()[1][0:5])<12:
                    time=i[10].split()[1][0:5]+'am'
                else:
                    time=i[10].split()[1][0:5]+'pm'
                dList.append({'marker_id':i[0],
                                'lng':i[1],
                                'lat':i[2],
                                'color':i[3],
                                'name':i[4],
                                'mtype':i[5],
                                'radius':i[6],
                                'subject':i[7],
                                'description':i[8],
                                'address':i[9].split(','),
                                'date':i[10].split()[0],
                                'time':time,
                                'user_id':i[11]
                                })
            resp={'query':'ok',
                        'data': str(dList)}
        except sa.exc.SQLAlchemyError:
            db.session.rollback()    
            resp={'query':'not_ok' }
        finally:
                db.session.close()
    return Response(
        json.dumps(resp)
    )

@my_map.route('/map/notifyNearby', methods=['GET','POST'])
def notifyNearby():
    resp={'query':''}
    if request.method == 'POST':
        request_data=request.get_json()
        subject=request_data['subject']
        message=request_data['message']
        clng=request_data['clng']
        clat=request_data['clat']
        radius=request_data['radius']
        user_id=request_data['user_id']
        recieverTypes=request_data['rTypes']

        rList=[]
        try:
            r=db.engine.execute('select lat,lng,user_id,name from marker')
            for i in r:
                if i[2] != user_id:
                    if i[3] in recieverTypes or 'all' in recieverTypes:
                        if MapFunctions.getrecArea(clat,clng,i[0],i[1],radius,i[2]):
                            rList.append(i[2])
                            #send message goes here
                            #make rList a set
            resp={'query':'ok'}
        except sa.exc.SQLAlchemyError:
            db.session.rollback()    
            resp={'query':'not_ok' }
        finally:
                db.session.close()
    return Response(
        json.dumps(resp)
    )

# @my_map.route("/map/message", methods=['GET','POST'])
# def message():
#     resp={
#     "status":"fail",
#     "data":{}
#     }
#     if request.method == 'POST':
#         request_data=request.get_json()

#         name=request_data['name']
#         message=request_data['message']
#         longitude=request_data['longitude']
#         lattitude=request_data['lattitude']
        
#         try:
#             mapMessage = MapMessage(name=name, message=message, longitude=longitude, lattitude= lattitude)
#             db.session.add(mapMessage)
#             db.session.commit()
#             resp={
#             "status":"success",
#             "data":{ "message sent":'ok'
#             }
#             }

#         except sa.exc.SQLAlchemyError:
#             db.session.rollback()
#             resp={
#             "status":"db_fail",
#             "data":{}
#             }

#     return Response(
#             json.dumps(resp),
#             mimetype='aplication/json',
#             headers={
#                 'Cache-Control' : 'no-cache',
#                 'Access-Control-Allow-Origin':'http://localhost:3000'
#             }
#         )

# ##################################################################################################
# #route notifyUser



# @my_map.route("/map/notify", methods=['GET','POST'])
# def notify():
#     resp={
#     }
    
#     # if request.method == 'POST':
#     #     request_data=request.get_json()

#     #     user_id=request_data['user_id']
#     #     subject=request_data['subject']
#     #     message=request_data['message']
#     #     radius=request_data['radius']
#     #     user_type=request_data['user_type']
#     #     location=request_data['my_location']
        
#     #     print(request_data)
#     #     # try:
#         #     mapMessage = MapMessage(name=name, message=message, longitude=longitude, lattitude= lattitude)
#         #     db.session.add(mapMessage)
#         #     db.session.commit()
#         #     resp={
#         #     "status":"success",
#         #     "data":{ "message sent":'ok'
#         #     }
#         #     }

#         # except sa.exc.SQLAlchemyError:
#         #     db.session.rollback()
#         #     resp={
#         #     "status":"db_fail",
#         #     "data":{}
#         #     }

#     return Response(
#             json.dumps(resp),
#             mimetype='aplication/json',
#             headers={
#                 'Cache-Control' : 'no-cache',
#                 'Access-Control-Allow-Origin':'*'
#             }
#         )

# # @my_map.route('/map/addUserLocation', methods=['GET,POST'])
# # def addLocation():
# #     resp={
# #     "status":"fail",
# #     "data":{}
# #     }
# #     if request.method == 'POST':
# #         request_data=request.get_json()

# #         user_id=request_data['user_id']
# #         lng=request_data['longitude']
# #         lat=request_data['lattitude']
        
# #         try:
# #             UserLocation = UserLocation(user_id=user_id, lng=lng, lat=lat)
# #             db.session.add(UserLocation)
# #             db.session.commit()
# #             resp={
# #             "status":"success",
# #             "data":{ "message sent":'ok'
# #             }
# #             }

# #         except sa.exc.SQLAlchemyError:
# #             db.session.rollback()
# #             resp={
# #             "status":"db_fail",
# #             "data":{}
# #             }

# #     return Response(
# #             json.dumps(resp),
# #             mimetype='aplication/json',
# #             headers={
# #                 'Cache-Control' : 'no-cache',
# #                 'Access-Control-Allow-Origin':'http://localhost:3000'
# #             }
# #         )

