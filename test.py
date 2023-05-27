import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.output(18, GPIO.LOW)
GPIO.output(23, GPIO.LOW)


GPIO.output(23, GPIO.HIGH) # Allume la LED
time.sleep(10) # Attend 1 seconde
GPIO.output(23, GPIO.LOW) # Éteint la LED