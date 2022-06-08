from flask import Flask
from flask import Flask, render_template, Response, request
import RPi.GPIO as GPIO
import time
import os
import datetime
import sys
import subprocess
import cv2
import numpy as np
import tensorflow as tf
import filetype
from PIL import Image, ImageOps
global capture
capture=0
model = tf.keras.models.load_model('rps_model.hdf5')
app = Flask(__name__,template_folder='templates')
x1=3
x2=3
x3=3
x4=3
x5=3
x6=3
Motor1A = 24
Motor1B = 23
Motor1E = 25
Motor2A = 14
Motor2B = 15
Motor2E = 18
Motor3A = 8
Motor3B = 7
Motor3E = 21
Motor4A = 12
Motor4B = 16
Motor4E = 20
servoPIN1 =27
servoPIN2=22
servoPIN3 =17
servoPIN4 =10
servoPIN5 =9
servoPIN6 =11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)# GPIO Numbering
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)
GPIO.setup(Motor3A,GPIO.OUT)
GPIO.setup(Motor3B,GPIO.OUT)
GPIO.setup(Motor3E,GPIO.OUT)
GPIO.setup(Motor4A,GPIO.OUT)
GPIO.setup(Motor4B,GPIO.OUT)
GPIO.setup(Motor4E,GPIO.OUT)
GPIO.setup(servoPIN1, GPIO.OUT)
GPIO.setup(servoPIN2, GPIO.OUT)
GPIO.setup(servoPIN3, GPIO.OUT)
GPIO.setup(servoPIN4, GPIO.OUT)
GPIO.setup(servoPIN5, GPIO.OUT)
GPIO.setup(servoPIN6, GPIO.OUT)
p1 = GPIO.PWM(servoPIN1, 50)
p2 = GPIO.PWM(servoPIN2, 50)
p3 = GPIO.PWM(servoPIN3, 50)
p4 = GPIO.PWM(servoPIN4, 50)
p5 = GPIO.PWM(servoPIN5, 50)
p6 = GPIO.PWM(servoPIN6, 50)
pwm1=GPIO.PWM(Motor1E,100)
pwm2=GPIO.PWM(Motor2E,100)
pwm3=GPIO.PWM(Motor3E,100)
pwm4=GPIO.PWM(Motor4E,100)
pwm1.start(50)
pwm2.start(50)
pwm3.start(50)
pwm4.start(50)
p1.start(0)
p2.start(0)
p3.start(0)
p4.start(0)
p5.start(0)
p6.start(0)
print ("Done")

def import_and_predict(image_data, model):
    size = (75,75)
    image = ImageOps.fit(image_data, size, Image.ANTIALIAS)
    image = image.convert('RGB')
    image = np.asarray(image)
    image = (image.astype(np.float32) / 255.0)
    img_reshape = image[np.newaxis,...]

    prediction = model.predict(img_reshape)
        
    return prediction

@app.route("/")
def index():
    return render_template('index1.html')


@app.route('/A')
def forward():
    data1="A"
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.HIGH)
    GPIO.output(Motor3A,GPIO.HIGH)
    GPIO.output(Motor3B,GPIO.LOW)
    GPIO.output(Motor3E,GPIO.HIGH)
    GPIO.output(Motor4A,GPIO.HIGH)
    GPIO.output(Motor4B,GPIO.LOW)
    GPIO.output(Motor4E,GPIO.HIGH)
    time.sleep(2)
    return render_template('index1.html')

@app.route('/a')
def backward():
    data1="a"
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)
    GPIO.output(Motor3A,GPIO.LOW)
    GPIO.output(Motor3B,GPIO.HIGH)
    GPIO.output(Motor3E,GPIO.HIGH)
    GPIO.output(Motor4A,GPIO.LOW)
    GPIO.output(Motor4B,GPIO.HIGH)
    GPIO.output(Motor4E,GPIO.HIGH)
    time.sleep(2)
    return render_template('index1.html')

@app.route('/B')
def left():
    data1="B"
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.LOW)
    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.HIGH)
    GPIO.output(Motor3A,GPIO.LOW)
    GPIO.output(Motor3B,GPIO.LOW)
    GPIO.output(Motor3E,GPIO.LOW)
    GPIO.output(Motor4A,GPIO.HIGH)
    GPIO.output(Motor4B,GPIO.LOW)
    GPIO.output(Motor4E,GPIO.HIGH)
    time.sleep(2)
    return render_template('index1.html')

@app.route('/b')
def right():
    data1="b"
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.LOW)
    GPIO.output(Motor3A,GPIO.HIGH)
    GPIO.output(Motor3B,GPIO.LOW)
    GPIO.output(Motor3E,GPIO.HIGH)
    GPIO.output(Motor4A,GPIO.LOW)
    GPIO.output(Motor4B,GPIO.LOW)
    GPIO.output(Motor4E,GPIO.LOW)
    time.sleep(2)
    return render_template('index1.html')

@app.route('/C')
def stop():
    data1="C"
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.LOW)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.LOW)
    GPIO.output(Motor3A,GPIO.LOW)
    GPIO.output(Motor3B,GPIO.LOW)
    GPIO.output(Motor3E,GPIO.LOW)
    GPIO.output(Motor4A,GPIO.LOW)
    GPIO.output(Motor4B,GPIO.LOW)
    GPIO.output(Motor4E,GPIO.LOW)
    file = "/home/pi/Trail/test.jpg"
    if filetype.is_image(file):
        image = Image.open(file)
        prediction = import_and_predict(image, model)
        if np.argmax(prediction) == 0:
            return render_template('index2.html')
        elif np.argmax(prediction) == 1:
            return render_template('index1.html')
    else:
        return render_template('index2.html')

@app.route('/d')
def botomservo1():
    data1="d"
    global x1
    x1=x1+1
    p1.ChangeDutyCycle(x1)
    return render_template('index1.html')
@app.route('/e')
def botomservo2():
    data1="e"
    global x1
    x1=x1-1
    p1.ChangeDutyCycle(x1)
    return render_template('index1.html')

@app.route('/f')
def firsthand1():
    data1="f"
    global x2
    x2+=1
    p2.ChangeDutyCycle(x2)
    return render_template('index1.html')
@app.route('/g')
def firsthand2():
    data1="g"
    global x2
    x2=x2-1
    p2.ChangeDutyCycle(x2)
    return render_template('index1.html')

@app.route('/h')
def secondhand1():
    data1="h"
    global x3
    x3+=1
    p3.ChangeDutyCycle(x3)
    return render_template('index1.html')
@app.route('/i')
def secondhand2():
    data1="i"
    global x3
    x3-=1
    p3.ChangeDutyCycle(x3)
    return render_template('index1.html')

@app.route('/j')
def thirdhand1():
    data1="j"
    global x4
    x4+=1
    p4.ChangeDutyCycle(x4)
    return render_template('index1.html')
@app.route('/k')
def thirdhand2():
    data1="k"
    global x4
    x4-=1
    p4.ChangeDutyCycle(x4)
    return render_template('index1.html')

@app.route('/l')
def forthhand1():
    data1="l"
    global x5
    x5+=1
    p5.ChangeDutyCycle(x5)
    return render_template('index1.html')
@app.route('/m')
def forthhand2():
    data1="m"
    global x5
    x5-=1
    p5.ChangeDutyCycle(x5)
    return render_template('index1.html')

@app.route('/n')
def cuter1():
    data1="n"
    global x6
    x6+=1
    p6.ChangeDutyCycle(x6)
    return render_template('index1.html')
@app.route('/o')
def cuter2():
    data1="o"
    global x6
    x6-=1
    p6.ChangeDutyCycle(x6)
    return render_template('index1.html')

camera = cv2.VideoCapture(1)
def gen_frames():
    global out, capture
    while True:
        success, frame = camera.read()
        if success:
            if(capture):
                print(capture)
                cv2.imwrite('/home/pi/Trail/test.jpg', frame)
                capture=0
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
        else:
            pass

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch,camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture=1
    elif request.method=='GET':
        return render_template('index1.html')
    return render_template('index1.html')

if __name__ == "__main__":
    print ("Strat")
    app.run(host='192.168.43.175', port=5010)
