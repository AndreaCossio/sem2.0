import serial
import pygame

pygame.init()
pygame.display.set_caption('ARDUINO-PROJECT')
screen = pygame.display.set_mode([1000, 600])
screen.fill ([255, 255, 255])

try:
    arduino = serial.Serial(
        port='COM9',\
        baudrate=9600,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
            timeout=0)
except:
    print 'ERROR OPENING SERIAL!!!!'
    print 'ERROR'
    print 'ERROR'
    arduino = open('arduino.txt', 'w')
choice = 'arduino'
command = 0
verse = 0
author = 2
arduino_command = 0
ending_command = 0
position = [0, 0]
calibrating = False
calibrating_done = False
arduino_right_step = False
arduino_left_step = False

arduino.write('2')
arduino.write('0')
arduino.write('0')

#COMMANDS:
#Sender == Python (0):
#   0: Rotate right motor for INFINITY
#   1: Rotate right motor for ONE STEP
#   2: Rotate left motor for INFINITY
#   3: Rotate left motor for ONE STEP
#   4: Rotate right motor for HALF STEP
#   5: Rotate left motor for HALF STEP
#   6: Right motor back to 0 []
#   7: Left motor back to 0 []
#Sender == ARDUINO (1):
#   0: A0 Photoresistor hit by right motor
#   1: A1 Photoresistor hit by right motor
#   2: Right motor DONE 1 STEP
#   3: A2 Photoresistor hit by left motor
#   4: A3 Photoresistor hit by left motor
#   5: Left motor DONE 1 STEP

print 'Calibration DEVICE!'
print 'Photoresistor order: A0, A1, A2, A3'
print 'COMMANDS'
print 'C: start calibration'
print 'RIGHT: one step right'
print 'LEFT: one step left'
print 'D: half a step right'
print 'A: half a step left'
print 'UP: one step UP'
print 'DOWN: one step down'
print 'w: half a step up'
print 's: half a step down'
print ' '

def chessboard_background ():
    for x in range (0, 12):
        for y in range (0, 12):
            if (y == 0) or (y == 11):
                color = [204, 51, 0]
                border_color = [204, 51, 0]
            elif (x == 0) or (x == 11):
                if (y == 0) or (y == 11):
                    color = [204, 51, 0]
                    border_color = [204, 51, 0]
            elif ((x / 2.0) == int(x / 2)):
                if (y / 2.0) == int(y / 2):
                    color = [50, 50, 50]
                    if (y == 1) or (y == 10):
                        color = [0, 0, 255]
                    if (x == 1)or (x == 10):
                        color = [0, 0, 255]
                else:
                    color = [200, 200, 200]
                    if (y == 1)or (y == 10):
                        color = [51, 153, 255]
                    if (x == 1) or (x == 10):
                        color = [51, 153, 255]
                border_color = [0, 0, 0]
            else:
                if (y / 2.0) == int(y / 2):
                    color = [200, 200, 200]
                    if (y == 1) or (y == 10):
                        color = [51, 153, 255]
                    if (x == 1) or (x == 10):
                        color = [51, 153, 255]
                else:
                    color = [50, 50, 50]
                    if (y == 1) or (y == 10):
                        color = [0, 0, 255]
                    if (x == 1) or (x == 10):
                        color = [0, 0, 255]
                border_color = [0, 0, 0]
            pygame.draw.rect(screen, color, [x*50, y*50, 50, 50], 0)
            pygame.draw.rect(screen, border_color, [x*50, y*50, 50, 50], 1)
    pygame.draw.rect(screen, [0, 0, 0], [0, 0, 600, 600], 1)

def arduino_print():
    global command, verse
    arduino.write('0')
    arduino.write(str(command))
    arduino.write(str(verse))

def arduino_read ():
    global arduino_command, author, ending_command
    try:
        serial_lenght = arduino.inWaiting()
    except:
        serial_lenght = 0
    if serial_lenght >= 3:
        author = arduino.read()
        arduino_command = arduino.read()
        ending_command = arduino.read()
        if author == '0':
            arduino.write('0')
            arduino.write(arduino_command)
            arduino.write(ending_command)

def deploy_machine ():
    global position, arduino_right_step, calibrating
    chessboard_background ()
    pygame.draw.rect(screen, [255, 0, 0] ,[position[0]*25 + 49, 50 , 2, 500], 0)
    pygame.draw.rect(screen, [255, 0, 0] ,[50, position[1]*25 + 49 , 500, 2], 0)
    if arduino_right_step:
        color = [0, 255, 0]
    else:
        color = [255, 0, 0]
    if calibrating:
        color = [255, 255, 0]
    pygame.draw.rect(screen, color ,[position[0]*25+40, position[1]*50+40 , 20, 20], 0)
    pygame.display.update ()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit ()
        elif event.type == pygame.KEYDOWN and event.key== pygame.K_RETURN:
            nothing = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            if calibrating == False:
                calibrating = True
                command = 0
                verse = 0
                arduino_print()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if calibrating_done:
                if position[0] <= 18:
                    if arduino_right_step:
                        position[0] += 2
                        command = 1
                        verse = 0
                        arduino_right_step = False
                        arduino_print()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            if calibrating_done:
                if position[0] >= 2:
                    if arduino_right_step:
                        position[0] -= 2
                        command = 1
                        verse = 1
                        arduino_right_step = False
                        arduino_print()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            if calibrating_done:
                if position[1] >= 2:
                    if arduino_left_step:
                        position[1] -= 2
                        command = 3
                        verse = 1
                        arduino_left_step = False
                        arduino_print()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            if calibrating_done:
                if position[1] <= 18:
                    if arduino_left_step:
                        position[1] += 2
                        command = 3
                        verse = 0
                        arduino_left_step = False
                        arduino_print()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            if calibrating_done:
                if position[0] <= 19:
                    if arduino_right_step:
                        position[0] += 1
                        command = 4
                        verse = 0
                        arduino_right_step = False
                        arduino_print()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            if calibrating_done:
                if position[0] >= 1:
                    if arduino_right_step:
                        position[0] -= 1
                        command = 4
                        verse = 1
                        arduino_right_step = False
                        arduino_print()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            if calibrating_done:
                if position[1] <= 19:
                    if arduino_left_step:
                        position[1] += 1
                        command = 5
                        verse = 0
                        arduino_left_step = False
                        arduino_print()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            if calibrating_done:
                if position[1] >= 1:
                    if arduino_left_step:
                        position[1] -= 1
                        command = 5
                        verse = 1
                        arduino_left_step = False
                        arduino_print()
    if author == '1':
        if arduino_command == '0':
            if ending_command == '0':
                if calibrating:
                    command = 0
                    verse = 1
                    arduino_print()
        elif arduino_command == '1':
            if ending_command == '1':
                if calibrating:
                    command = 2
                    verse = 0
                    arduino_print()
        elif arduino_command == '2':
            arduino_right_step = True
        elif arduino_command == '3':
            if ending_command == '0':
                if calibrating:
                    command = 2
                    verse = 1
                    arduino_print()
        elif arduino_command == '4':
            if ending_command == '1':
                if calibrating:
                    calibrating = False
                    calibrating_done = True
                    arduino_right_step = True
                    arduino_left_step = True
        elif arduino_command == '5':
            arduino_left_step = True
        author = ''
        arduino_command = ''
        ending_command = ''
    arduino_read ()
    deploy_machine()
    pygame.display.update ()


