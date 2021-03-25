# ASST

This is the source code for the IOT device to be used with [this](https://github.com/coldkillerr/ASST_Django) application

## Hardware requirements :

1) [Raspberry pi 3b+](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/)
2) [Pi Camera](https://www.raspberrypi.org/products/raspberry-pi-high-quality-camera/)
3) [MLX90614](https://www.amazon.com/HiLetgo-MLX90614ESF-Non-contact-Infrared-Temperature/dp/B071VF2RWM/ref=sr_1_3?dchild=1&keywords=MLX90614&qid=1616657397&sr=8-3) for temperature detection.

## Setting up the hardware components

1) [Configure camera with raspberry pi](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera)
2) [Configure MLX90614 temperature Sensor](https://circuitdigest.com/microcontroller-projects/iot-based-contactless-body-temperature-monitoring-using-raspberry-pi-with-camera-and-email-alert)

## Starting the device

1) Create a project [here](https://console.firebase.google.com/u/0/)

2) Download the credentials.json from  [firebase project settings](https://console.firebase.google.com). Paste the path to credentials 
[here](https://github.com/coldkillerr/ASST_IOT/blob/cd71ae63c79d93c29a71d1fa20225085f33140c4/config.py#L4)

3) Get the firebase SDK snippet from  [firebase project settings](https://console.firebase.google.com). Paste it [here](https://github.com/coldkillerr/ASST_IOT/blob/cd71ae63c79d93c29a71d1fa20225085f33140c4/config.py#L4)

4) Create a virtual environment with
``` 
python3 -m virtualenv yourenv
```
5) Navigate to the project directory and install the requirements with 
```
pip3 install -r requirements.txt
```
6) Start the device with 

```
python3 main.py
```
