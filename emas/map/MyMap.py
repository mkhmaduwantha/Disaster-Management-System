import math

class MyMap:
    #constructor goes here
    def __init__(self,my_lat, my_lng):
        super().__init__()
        self.my_lat= my_lat
        self.mt_lng= my_lng
    
    #calculate the distance between two given geolocations on the map
    #return distance in KM
    def _calDistBtw2Point(self, center_lat, center_lng, end_lat, end_lng):
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

    #calclulate the reciever is within the given distance or not
    #return true or false if the user is within the area or not
    def getrecArea(self, center_lat, center_lng, end_lat, end_lng, radius, user_id):
        dist=self._calDistBtw2Point(center_lat, center_lng, end_lat, end_lng)
        if(radius<dist):
            return True
        else:
            return False
    
    





    
