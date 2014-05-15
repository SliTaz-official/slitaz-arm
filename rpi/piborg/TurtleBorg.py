#!/usr/bin/env python
# coding: Latin-1

# Load library functions we want
import sys
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set which GPIO pins the drive outputs are connected to
DRIVE_1 = 4
DRIVE_2 = 18
DRIVE_3 = 8
DRIVE_4 = 7

# Set all of the drive pins as output pins
GPIO.setup(DRIVE_1, GPIO.OUT)
GPIO.setup(DRIVE_2, GPIO.OUT)
GPIO.setup(DRIVE_3, GPIO.OUT)
GPIO.setup(DRIVE_4, GPIO.OUT)

# Map of functions to drive pins
leftDrive = DRIVE_1                     # Drive number for left motor
rightDrive = DRIVE_4                    # Drive number for right motor
penDrive = DRIVE_3                      # Drive number for pen solenoid

# Functions for the robot to perform
def MoveForward(n):
    """Move forward for 'n' seconds"""
    GPIO.output(leftDrive, GPIO.HIGH)
    GPIO.output(rightDrive, GPIO.HIGH)
    time.sleep(n)
    GPIO.output(leftDrive, GPIO.LOW)
    GPIO.output(rightDrive, GPIO.LOW)

def MoveLeft(n):
    """Move left for 'n' seconds"""
    GPIO.output(leftDrive, GPIO.HIGH)
    GPIO.output(rightDrive, GPIO.LOW)
    time.sleep(n)
    GPIO.output(leftDrive, GPIO.LOW)

def MoveRight(n):
    """Move right for 'n' seconds"""
    GPIO.output(leftDrive, GPIO.LOW)
    GPIO.output(rightDrive, GPIO.HIGH)
    time.sleep(n)
    GPIO.output(rightDrive, GPIO.LOW)

def PenUp(n):
    """Lift the pen up"""
    GPIO.output(penDrive, GPIO.LOW)

def PenDown(n):
    """Place the pen down"""
    GPIO.output(penDrive, GPIO.HIGH)

def HelpMessage(n):
    """Display a list of available commands"""
    print ''
    print 'Available commands:'
    commands = dCommands.keys()
    commands.sort()
    for command in commands:
        print '% 10s - %s, %s' % (command, dCommands[command].func_name, dCommands[command].__doc__)
    print ''

# Map of command names to functions
dCommands = {
        'FORWARD':MoveForward,
        'FD':MoveForward,
        'LEFT':MoveLeft,
        'LT':MoveLeft,
        'RIGHT':MoveRight,
        'RT':MoveRight,
        'PENUP':PenUp,
        'PU':PenUp,
        'PENDOWN':PenDown,
        'PD':PenDown,
        'HELP':HelpMessage,
        '?':HelpMessage
        }

# If we have been run directly then look at command line
if __name__ == "__main__":
    # Process command
    if len(sys.argv) > 1:
        # Extract the command name and value (if there is any)
        command = sys.argv[1].upper()
        if len(sys.argv) > 2:
            sValue = sys.argv[2].upper()
        else:
            sValue = '0'
        try:
            fValue = float(sValue)
        except:
            fValue = 0.0
    
        # Select the appropriate function and call it
        if dCommands.has_key(command):
            dCommands[command](fValue)
        else:
            print 'Command "%s" not recognised' % (command)
            HelpMessage(fValue)
    else:
        # No command, display the help message
        print 'Usage: %s command [n]' % (sys.argv[0])
        HelpMessage(0)

    
