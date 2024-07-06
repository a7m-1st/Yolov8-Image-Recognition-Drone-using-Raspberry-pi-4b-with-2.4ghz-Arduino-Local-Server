import firebase_admin
from firebase_admin import db, credentials
import time
from serial import Serial
import calculate_gps
import math



#Insert Object
def calculate_gps(obj, gps_lat, gps_long):
    import math
    obj_dist = 0

    
    #Normalized Pixels of each object
    xp = obj['xcor']
    yp = obj['ycor']

    #Scaling to equation resolution
    #Orig= 1080x720 want=4032x3024
    xp *= (4032/1080)
    yp *= (3024/720)

    x_origin = (4032/2) #Middle point
    x_dist = abs(x_origin - xp) #shift from middle point
    # print('x distance of object is ', round(x_dist))


    #Horizontal Hypotenuse = Max distance considering side
    print('original distance ', 0.11619*yp - 0.5176)

    dx = 0.11619*x_dist - 0.5176 #Want: Meters given x dist px returns in Meters
    #print('dx (Horizontal) is ', dx)

    yp = math.sqrt(yp**2 + x_dist**2) #Y px + X px
    #angle = 'xyz' #get angle

    #This equation is 2 dimentional
    obj_dist = 0.11619*yp - 0.5176 #returns in meters

    #Adding Altitude
    alt = obj['altitude'] #~100m
    #print('objdist before altitude is ', round(obj_dist/100, 2), ' with alt of ', alt)

    dy = obj_dist #Y i.e. right-left
    #print('dy is (vertical) ', dy)

    #obj_dist = math.sqrt(obj_dist**2 + alt**2) #what is alt represented in pixels??
    obj_dist = 0.018*alt**2+ 0.11619*yp-0.5176

    print("predestrian is ", round(obj_dist/100, 2), "m away from origin. \n")

    

    r_earth = 6378
    new_latitude  = gps_lat  + ((dy/100000) / r_earth) * (180 / math.pi)
    new_longitude = gps_long + ((dx/100000) / r_earth) * (180 / math.pi) / math.cos(gps_lat * math.pi/180)

    print('Old Latitude ', gps_lat, ' new Lat ', new_latitude, '\n')
    print('Old Longitude ', gps_long, ' new Long ', new_longitude, '\n')
    return [new_latitude, new_longitude]



def initialize_db():
    cred = credentials.Certificate("credentials.json")
    firebase_admin.initialize_app(cred, {"databaseURL": "firebaseURL"})

#Good
def send_database(lat, lng, type):
    
    #Getting- db.reference("/").get()
    #Setting- db.reference("/videos").set(val) | Replaces value
    #Updating- db.reference("/").update({"subscribed": True}) | addes new node if non existant
    #Appending (pushing) - db.reference("/videos").push().set(val)

    #Add as an array of strings
    if(type != 0):
        latitude = lat
        longitude = lng
        db.reference("latitude").set(latitude)
        db.reference("longtitude").set(longitude)
    else:
        db.reference("/gps_lat").set(str(lat))
        db.reference("/gps_lng").set(str(lng))

    if(type > 1):
        #Show data
        ref = db.reference("/")
        print(ref.get())

def reset_fields():
    db.reference('/').update({'latitude':[]})
    db.reference('/').update({'longtitude':[]})



# coor = calculate_gps(
#                 {
#                     'xcor': 655.15,
#                     'ycor': 480.85,
#                     'altitude': 50
#                 }
#                 ,gps_lat= 3.12
#                 ,gps_long= 101.64
#             )

# lat = lng = 0
# coor[0] = lat
# coor[1] = lng

# print(lat, ' ', lng)
    