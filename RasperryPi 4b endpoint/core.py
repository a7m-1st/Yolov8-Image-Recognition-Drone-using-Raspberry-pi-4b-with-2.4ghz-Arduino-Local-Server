from ultralytics import YOLO

# Load a model
model = YOLO('Model/Copyofbest.pt')  # load a pretrained model (recommended for training)


# Train the model
# results = model.train(data='VisDrone.yaml', epochs=100, imgsz=640, project = '/content/drive/MyDrive/RoboIot', resume=True)



import cv2, random
import time
from ultralytics.utils.plotting import Annotator  # ultralytics.yolo.utils.plotting is deprecated

#Capture Videos
# cap = cv2.VideoCapture(0)
# cap.set(3, 640)
# cap.set(4, 480)
box_info_list = []

name = model.names
#generate random R G B for each name
colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(model.names))]

# for i in range(2):
def process_image(img, show):
    box_info_list = []
    img2 = img
    classes = [0, 1]
    if(show):
        cap = cv2.VideoCapture('Content/Videos/New York Flooding Chaos - Brooklyn - Long Island  - Raw 4k with Drone.mp4')
    
        #Read Frames
        ret, img = cap.read()
        print('getting video image')
        #If no image
        if not ret:
            print("No image read")
            pass
            
        classes = [0, 1, 2, 3, 4, 5]

    # BGR to RGB conversion is performed under the hood
    # see: https://github.com/ultralytics/ultralytics/issues/2575
    results = model.predict(img, conf=0.50, classes=classes) #confidence >= 50%

    for r in results:
        annotator = Annotator(img)

        boxes = r.boxes
        for box in boxes:
            b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
            c = box.cls
            name = model.names[int(c)]
            print(box.xywh[0], name)

            #Adding confidence label
            confidence = box.conf.item()*100
            label_with_confidence = f"{model.names[int(c)]} {confidence:.2f}"

            annotator.box_label(b, label_with_confidence, color=colors[int(c)])

            #How to differentiate objects???
            coordinates = box.xywh[0].cpu().numpy()
            
            box_info_list.append({
                'total': len(boxes),
                'xcor': coordinates[0],
                'ycor': coordinates[1],
                'confidence': confidence,
            })
            

    img = annotator.result()
#     if(show):
#         cv2.imshow("Processed Output.jpg", img)
#         cv2.waitKey(0)
    
    #print('box info list is ', box_info_list)
    return box_info_list




import serial
import time
import string
import pynmea2

def get_gps():
    lat = 0
    alt = 0
    lng = 0
   
    print('loop entered')
    port="/dev/ttyS0"
    ser=serial.Serial(port, baudrate=9600, timeout=0.5)
    dataout = pynmea2.NMEAStreamReader()
    newdata=ser.readline()
    newdata=ser.readline()
    newdata=ser.readline()

    newdata = newdata.decode('utf-8')
    if newdata[0:6] == "$GPGGA":
        newmsg=pynmea2.parse(newdata)
        lat=newmsg.latitude
        lng=newmsg.longitude
        alt=newmsg.altitude
        gps = "Latitude=" + str(lat) + " and Longitude=" + str(lng) + " Alt = " + str(alt)
        print(gps)
    time.sleep(0.5)
        
    if(alt is None):
        alt = 0.00;
    return [lat, lng, alt, 0]
    



"""
Simple example of using the RF24 class.
"""
import sys
import argparse
import time
import struct
from pyrf24 import RF24, RF24_PA_LOW


########### USER CONFIGURATION ###########
radio = RF24(22, 0)

# using the python keyword global is bad practice. Instead we'll use a 1 item
# list to store our float number for the payloads sent



# For this example, we will use different addresses
# An address need to be a buffer protocol object (bytearray)
address = [b"1Node", b"2Node"]
# It is very helpful to think of an address as a path instead of as
# an identifying device destination

# to use different addresses on a pair of radios, we need a variable to
# uniquely identify which address this radio will use to transmit
# 0 uses address[0] to transmit, 1 uses address[1] to transmit
print("Which radio is this? Enter '0' or '1'. Defaults to '0' ")
radio_number = bool(1)

# initialize the nRF24L01 on the spi bus
if not radio.begin():
    raise OSError("nRF24L01 hardware isn't responding")

# set the Power Amplifier level to -12 dBm since this test example is
# usually run with nRF24L01 transceivers in close proximity of each other
radio.set_pa_level(RF24_PA_LOW)  # RF24_PA_MAX is default

# set TX address of RX node into the TX pipe
radio.open_tx_pipe(address[0])  # always uses pipe 0

# set RX address of TX node into an RX pipe
radio.open_rx_pipe(1, address[1])  # using pipe 1

# To save time during transmission, we'll set the payload size to be only what
# we need. A float value occupies 4 bytes in memory using struct.calcsize()
# "<f" means a little endian unsigned float
radio.payload_size = struct.calcsize("ffff")

# for debugging
radio.print_details()

payload = [0, 0, 0, 0]

def master(flag, data):  # count = 5 will only transmit 5 packets
    payload = gps = get_gps()
    while(gps[0] == 0):
        print('No data recieved.. Trying again')
        payload = get_gps()
        gps = payload
        payload[3] = len(data)
        print('data length is ', payload[3])
        
        if(gps[0] == 0 and flag):
            gps = payload = [3.1588, 101.6956, 500, len(data)]
    
    print("data recieved is ", payload)
    print("data in param is ", data)

    
    
    """Transmits an incrementing float every second"""
    radio.listen = False  # ensures the nRF24L01 is in TX mode
    count = 1
    
    for i in range(2):
        if count != 1:
            print('Loop Entered Phase II')
            for j in range(len(data)):
            ##Transfer Data afterwards
                payload = data[j]
                print('i payload is ;', payload)
                #use struct.pack() to pack your data into a usable payload
                # into a usable payload
                buffer = struct.pack("fff", *payload)
                # "<f" means a single little endian (4 byte) float value.
                start_timer = time.monotonic_ns()  # start timer
                result = radio.write(buffer)
                end_timer = time.monotonic_ns()  # end timer

                if not result:
                    print("Transmission failed or timed out, buffer is ", buffer)
                else:
                    print(
                        "Transmission successful! Time to Transmit:",
                        f"{(end_timer - start_timer) / 1000} us. Sent: {payload}",
                    )
                    #payload[0] += 0.01
                time.sleep(1)
                
        else:                 
            # use struct.pack() to pack your data into a usable payload
            # into a usable payload
            buffer = struct.pack("ffff", *payload)
            # "<f" means a single little endian (4 byte) float value.
            start_timer = time.monotonic_ns()  # start timer
            result = radio.write(buffer)
            end_timer = time.monotonic_ns()  # end timer

            if not result:
                print("Transmission failed or timed out, buffer is ", buffer)
            else:
                print(
                    "Transmission successful! Time to Transmit:",
                    f"{(end_timer - start_timer) / 1000} us. Sent: {payload}",
                )
                #payload[0] += 0.01
            time.sleep(0.5)
            
        count = count+1
        

print(sys.argv[0])  # print example name


from time import sleep
import cv2

def get_image(show):
    cv2.destroyAllWindows()
    import os
    #-v 0 is 0 verbose: set to 1 / 2 for debugging
    #--vflip
    os.system("libcamera-jpeg -o ./Capture/output.jpg -t 1000 --vflip --width 1920 --height 1080 -n -v 0")
    
    img = cv2.imread("./Capture/output.jpg")
    if(show):
        cv2.imshow("output.jpg", cv2.resize(img, (960, 540)))
        sleep(2)
        cv2.destroyAllWindows()
        
    return img


import threading
import numpy

#Set process_img True to use stock video,
#Set master True to use stock gps location
if __name__ == "__main__":

    try:
        while True:
            #Process the Image
            print('getting image')
            img = get_image(False)
            print('gotten image')
            box_info_list = process_image(img, False)
            print("EXITED IMAGE SUCESSFULLY")

            #print('box info is ', box_info_list)
            if(len(box_info_list) is not 0): 

                data = []
                for obj in box_info_list:
                    #print('the length of box info is ', box_info_list)
                    data.append([obj['xcor'], obj['ycor'], 1])

                #print('looks like ', numpy.array(data))

                radio_thread = threading.Thread(target= master, args=(True, numpy.array(data),))
                radio_thread.start()
                radio_thread.join()

        
        #instead of cv2.imshow('Subtitle', img)
        #cv2.imshow('Processed image.jpg', img)
        #Pause
        if cv2.waitKey(1) & 0xFF == ord(' '):
            print(" Keyboard Interrupt detected. Exiting...")
            radio.power = False
            sys.exit()
        
    except KeyboardInterrupt:
        print(" Keyboard Interrupt detected. Exiting...")
        radio.power = False
        sys.exit()
        cap.release()
        cv2.destroyAllWindows()
        
else:
    print("    Run slave() on receiver\n    Run master() on transmitter")
    
# cap.release()
# cv2.destroyAllWindows()




