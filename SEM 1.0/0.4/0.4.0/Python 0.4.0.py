import serial
import pygame

pygame.init()
pygame.display.set_caption('ARDUINO-PROJECT')
screen = pygame.display.set_mode([1000, 600])
screen.fill ([255, 255, 255])

arduino = serial.Serial(
    port='COM9',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)
choice = 'arduino'
command = 0
author = 0
arduino_command = 0

def arduino_print():
    global command
    arduino.write('0')
    arduino.write(str(command))

def arduino_read ():
    global arduino_command, author
    try:
        serial_lenght = arduino.inWaiting()
        if serial_lenght >= 2:
            author = arduino.read()
            arduino_command = arduino.read()
            #for line in arduino.read():
                
                #result = line
            #result = arduino.read()
    except:
        print 'entered in except'
        nothing = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit ()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            arduino_print()
            screen.fill ([255, 255, 255])
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            command = 0
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
            command = 1
    if author == '1':
        if arduino_command == '5':
            screen.fill ([255, 0, 0])
            #command = 0
            #arduino_print ()
    arduino_read ()
    #arduino.write(command + '\n')
    #arduino.write(second_command + '\n')oooo
    #arduino.write(third_command)
    pygame.display.update ()