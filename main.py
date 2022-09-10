from picamera import PiCamera
from time import sleep
import os
import cv2
import sys
import RPi.GPIO as GPIO

pirPin = 36 # Motion sensor
servoPin = 12

GPIO.setmode(GPIO.BOARD) # use PHYSICAL GPIO Numbering

GPIO.setup(pirPin, GPIO.IN) # set sensorPin to INPUT mode

GPIO.setup(servoPin, GPIO.OUT) # Set servoPin to OUTPUT mode
GPIO.output(servoPin, GPIO.LOW) # Make servoPin output LOW level

OFFSE_DUTY = 0.5
SERVO_MIN_DUTY = 2.5+OFFSE_DUTY
SERVO_MAX_DUTY = 12.5+OFFSE_DUTY

AngleYOffset = 1.000 # adjust for camera inaccuracy
AngleXOffset = 1.000
yOffset = 0 # adjust for distance between camera and motors
xOffset = 0
z = 109 # dist from camera to wall (in)
xRight = 500    # x maximum
xLeft = 500     # x minimum
yUp = 600       # y maximum
yDown = 200     # y minimum
heightUp = 40   # dist above 0,0 to y max (in)
heightDown = 20 # dist below 0,0 to y min (in)
widthRight = 30 # dist right of 0,0 to x max (in)
widthLeft = 30  # dist left of 0,0 to x min (in)

global p

p = GPIO.PWM(servoPin, 50) # set Frequece to 50Hz
p.start(0)

imagePath = "/home/pi/FRAAPL/frame.jpg"
cascPath = "/home/pi/FRAAPL/default.xml"

camera = PiCamera()
camera.start_preview()
sleep(5)

def map( value, fromLow, fromHigh, toLow, toHigh):
    return (toHigh-toLow)*(value-fromLow) / (fromHigh-fromLow) + toLow


def servoWrite(angle): # make the servo rotate to specific angle, 0-180
    angle = int(angle)
    if(angle < 0):
        angle = 0
    elif(angle > 180):
        angle = 180
    p.ChangeDutyCycle(map(angle,0,180,SERVO_MIN_DUTY,SERVO_MAX_DUTY)) 

def stepperWrite(angle):
    pass

def getAngleY(y):
    if y >= 0:
        yDist = (y/yUp) * heightUp
        angle = math.tan(yDist/z)
    else:
        y = math.abs(y)
        yDist = (y/yDown) * heightDown
        angle = math.tan(yDist/z)
    return angle * AngleYOffset

def getAngleX(x):
    if x >= 0:
        xDist = (x/xRight) * widthRight
        angle = math.tan(xDist/z)
    else:
        x = math.abs(x)
        xDist = (x/xLeft) * widthLeft
        angle = math.tan(xDist/z)
    return angle * AngleXOffset

def move(coords):
    cp = coords.split(',')
    x = int(cp[0] - xOffset)
    y = int(cp[1] - yOffset)
    yAngle = getAngleY(y)
    xAngle = getAngleX(x)
    servoWrite(yAngle)
    stepperWrite(xAngle)

def fire(coords):
    move(coords)
    # Set solinoid optocoupler to high

def getcoords():

    camera.capture('/home/pi/FRAAPL/frame.jpg')

    faceCascade = cv2.CascadeClassifier(cascPath)

    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.5,
        minNeighbors=5,
        minSize=(30, 30),
#    flags = cv2.CV_HAAR_SCALE_IMAGE
    )
#    print(type(faces[0]))
    print("Found {0} faces!".format(len(faces)))
    try:
        x = str(faces[0][0])
        y = int(str(faces[0][1]))
        y = str(abs(y - 500))
        coords = x + "," + y
        #    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #cv2.imwrite('faces.jpg', image)
        print(coords)
    except:
        coords = None
    return coords

servoWrite('90')
stepperWrite('90')

try:
    while True:
#    if GPIO.input(sensorPin)==GPIO.HIGH:
        coords = getcoords()
        print(coords)
        #if not coords is None:
        #    fire(coords)
        sleep(1)
    #else:
except KeyboardInterrupt:
    camera.stop_preview()
