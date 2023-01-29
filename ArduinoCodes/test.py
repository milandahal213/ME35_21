import time
from motorController import *
from machine import ADC, Pin, I2C
from lsm6dsox import LSM6DSOX
board = NanoMotorBoard()
print("reboot")
board.reboot()

time.sleep_ms(500)
#Defining sensor and potentiometer pins
sensor=ADC(Pin(28))
pot=ADC(Pin(29))

#creating training data
trainingData=[]
acceldata=[]
#defining imu pins
lsm = LSM6DSOX(I2C(0, scl=Pin(13), sda=Pin(12)))
def howmanytaps(acceldata): #if the board is horizontal and tapped on the usb port
    temp=1
    count=0
    valid=True
    for i in acceldata:
        if(i<0.99):
            valid=True
         else:
             if(valid):
                 count+=1
              else:
                  pass
              valid=False    
    print(count)
    return count             
while True:
    position=180*pot.read_u16()/60000 #mapping position to angle
    Servo(0).setAngle(position) #moving servo to the angle
    time.sleep(0.1)
    sens=sensor.read_u16() #reading sensor value
    if (lsm.read_accel()[2]<0.99):
        for i in range(10):
            acceldata.append(lsm.read_accel()[2])
            time.sleep(0.1)
        count=howmanytaps(acceldata)
        acceldata=[]
        if(count==1):
            trainingData.append([sens,position])
        elif(count>1):
            print(trainingData)
            while(True):
                min=65000
                sens=sensor.read_u16()
                for i in trainingData:
                    if(min>abs(sens-i[0])):
                        pos=i[1]
                        min=abs(sens-i[0])
                Servo(0).setAngle(pos)
                time.sleep(0.1)
     time.sleep(0.1)

  
  