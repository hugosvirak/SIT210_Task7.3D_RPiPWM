import RPi.GPIO as GPIO
import time

# Relating to the ultrasonic sensor, some of the circuit and code were followed from this tutorial: https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi

ultrasonicTriggerPin = 4
ultrasonicEchoPin = 27

buzzerPin = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzerPin,GPIO.OUT)
GPIO.setup(ultrasonicTriggerPin,GPIO.OUT)
GPIO.setup(ultrasonicEchoPin,GPIO.IN)

buzzerPwm = GPIO.PWM(buzzerPin, 500)
buzzerPwm.start(0)

def getMeasurement():
    
    # send pulse trigger
    GPIO.output(ultrasonicTriggerPin, True)
    time.sleep(0.00001)
    GPIO.output(ultrasonicTriggerPin, False)
    
    print("Getting Pulse")
    
    # get pulse
    while GPIO.input(ultrasonicEchoPin) == 0:
        pulseStart = time.time()
    while GPIO.input(ultrasonicEchoPin) == 1:
       pulseEnd = time.time()
    
    # calculate distance
    duration = pulseEnd - pulseStart
    distance = duration * 17150
    distance = min(distance, 50) # maximum value is 50
    distance = max(distance, 0) # minimum value is 0
    distance = distance * 2 # convert to out of 100 to make easier to work with
    return distance


time.sleep(1)
try:
    while (True):
        distance = getMeasurement()

        print(distance)
        buzzerPwm.ChangeDutyCycle(100 - distance)
        buzzerPwm.ChangeFrequency((100 - distance) * 50 + 1)

        
        time.sleep(0.2)
except KeyboardInterrupt:
    GPIO.cleanup()
