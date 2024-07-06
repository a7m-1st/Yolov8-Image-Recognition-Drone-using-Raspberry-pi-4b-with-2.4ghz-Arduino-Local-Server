# Runner up for Mranti/Universiti Malaya RoboIoT competetion 2024- Software & Tech Division

# Robo-IoT-2024 (yolov8 model not included)
Robo IoT drone project held between 25-Sep-2023 to 16-Mar-2024, this repository contains Software Backend used inside raspberry pi 4b

# Advantages
- Recognize Civilians from live drone footage (pi camera)
- Calculate the distance and perform coordinate translation from object position in image
- Transfer Lat & Long to Realtime Firebase database
- Rspi Module doesnt need wifi
- Operates with antenna range upto 1000m*
- Realtime data

# Challenges overcame
- Making NRF24L01+ inter communicate with Arduino Uno from Raspberry pi 4b
- Extracting the object coordinates from yolov8 model (using box.xyxy[0])
- Translating pixels to long & lat (needs optimization)
- Running vision model, taking picture, getting gps location and sending data simultaneously
- Taking Photo from pi camera was a challenge (had to resort to saving the photo to folder then extracting the saved image)
- Sending the gps & img coordinate payload through NRF24L01+ for each civilian to arduino Uno
- Getting Arduino Uno live data output from the Serial port with Python
  
# Tech Required
(Drone)
- Raspberry pi 4b
- Pi camera
- Neo 6m Gps
- NRF24L01+ Transmitter & Reciever


(Client)
- Laptop with Python installed
- Arduino Uno or any other
- NRF24L01+ Transmitter & Reciever



