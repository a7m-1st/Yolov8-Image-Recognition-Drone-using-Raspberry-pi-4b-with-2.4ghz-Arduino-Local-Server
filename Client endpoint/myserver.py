import firebase_admin
from firebase_admin import db, credentials
import time
from serial import Serial
import calculate_gps

#Install pyserial instead of serial as python -m install pyserial
#Close the serial monitor in arduino Ide
arduinoData = Serial('com7', 115200)
time.sleep(1)


length = 0
gps_lat = 0
gps_lng = 0
save_lat = save_lng = []
counter = 0
calculate_gps.initialize_db()
calculate_gps.reset_fields()

while True:
    #Keep looping untill data
    while(arduinoData.in_waiting == 0):
        pass

    dataPacket=arduinoData.readline()
    dataPacket=dataPacket.decode('utf-8')

    packet = []
    
    latitude = longitude = altitude = 0
    pastLength = [0]
    try:

        packet = [float(num) for num in dataPacket.split()]
        print(packet)


        #//gps is when p[3] is len(data) | lat, lng, alt, data-len
        #//data is                       | Xcor, ycor, 1
        #if it is normal coordinates
        
        
        #Send gps coordinates
        
        flag = True
        if(packet[2] != 1 and packet[0] != 0):
            length = 0
            pastLength.append(length)

            #If max is there, then no need to add
            if(max(pastLength) != 0):
                if(max(pastLength) < length):
                    flag = False
            elif flag and counter == length: #When the current len is greater than past
                #Reset the Database & add new
                calculate_gps.reset_fields()

            counter = 0
            save_lat = save_lng = []

            gps_lat = packet[0]
            gps_lng = packet[1]
            altitude = packet[2]
            length = packet[3]
            print('Saving gps coordinates of (ln 38) ', gps_lat, " ", gps_lng)
            calculate_gps.send_database(gps_lat, gps_lng, 0)


        if (flag and packet[2] == 1.0 and packet[0] != 0) :
            print('inside the pack')

            #Input: Lat & Lng
            lat, lng = calculate_gps.calculate_gps(
                {
                    'xcor': packet[0],
                    'ycor': packet[1],
                    'altitude': altitude
                }
                ,gps_lat= gps_lat
                ,gps_long= gps_lng
            )

            print('sending to db')
            save_lat.append(str(lat))
            save_lng.append(str(lng))
            calculate_gps.send_database(save_lat, save_lng, 1)
            counter += 1
        

        #Reset the length
        if(counter == length and not flag):
            length = 0
            counter = 0
            save_lat = save_lng = []

    except ValueError as e:
        print("error", e,"on",dataPacket)