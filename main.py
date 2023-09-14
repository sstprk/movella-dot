# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 11:59:42 2023

@author: Salih
"""
from vpython import *
from xdpchandler import *
import funcs
import movelladot_pc_sdk

if __name__ == "__main__":
    xdpcHandler = XdpcHandler()

    if not xdpcHandler.initialize():
        xdpcHandler.cleanup()
        exit(-1)

    xdpcHandler.scanForDots()
    if len(xdpcHandler.detectedDots()) == 0:
        print("No Movella DOT device(s) found. Aborting.")
        xdpcHandler.cleanup()
        exit(-1)

    xdpcHandler.connectDots()

    if len(xdpcHandler.connectedDots()) == 0:
        print("Could not connect to any Movella DOT device(s). Aborting.")
        xdpcHandler.cleanup()
        exit(-1)

    for device in xdpcHandler.connectedDots():

        print(f"Current profile: {device.onboardFilterProfile().label()}")
        if device.setOnboardFilterProfile("General"):
            print("Successfully set profile to General")
        else:
            print("Setting filter profile failed!")
            print("Trying again..")
            if device.setOnboardFilterProfile("General"):
                print("Successfully set profile to General")
            else:
                print("Setting filter profile failed!")
        
        #Logging option
        while(True):
            inpt = input("Logging data on/off?") 
            if inpt == "on":
                print("Setting quaternion CSV output")
                device.setLogOptions(movelladot_pc_sdk.XsLogOptions_Quaternion)
        
                logFileName = "logfile_" + device.bluetoothAddress().replace(':', '-') + ".csv"
                print(f"Enable logging to: {logFileName}")
                if not device.enableLogging(logFileName):
                    print(f"Failed to enable logging. Reason: {device.lastResultText()}")
                break
            elif inpt == "off":
                print("Disabled logging")
                break
            else:
                print("Warning! Pick one setting.")
            
        print("Putting device into measurement mode.")
        if not device.startMeasurement(movelladot_pc_sdk.XsPayloadMode_ExtendedQuaternion):
            print(f"Could not put device into measurement mode. Reason: {device.lastResultText()}")
            xdpcHandler.cleanup()
            exit(-1)

if device.startMeasurement(movelladot_pc_sdk.XsPayloadMode_ExtendedQuaternion):
    scene.range = 5
    scene.background = color.white
    scene.width = 950
    scene.height = 700
    
    xarrow = arrow(length=100, shaftwidth=.03, color=color.black, axis=vector(1,0,0))
    negxarrow = arrow(length=100, shaftwidth=.03, color=color.black, axis=vector(-1,0,0))
    labelx = label(pos=vector(3,0,0), text="X", box=0, line=0)
    yarrow = arrow(length=100, shaftwidth=.03, color=color.black, axis=vector(0,1,0))
    negyarrow = arrow(length=100, shaftwidth=.03, color=color.black, axis=vector(0,-1,0))
    labely = label(pos=vector(0,3,0), text="Y", box=0, line=0)
    zarrow = arrow(length=100, shaftwidth=.03, color=color.black, axis=vector(0,0,1))
    negzarrow = arrow(length=100, shaftwidth=.03, color=color.black, axis=vector(0,0,-1))
    labelz = label(pos=vector(0,0,3), text="Z", box=0, line=0)
    
    frontArrow=arrow(length=4,shaftwidth=.05,color=color.purple,axis=vector(1,0,0))
    upArrow=arrow(length=1,shaftwidth=.05,color=color.magenta,axis=vector(0,1,0))
    sideArrow=arrow(length=2,shaftwidth=.05,color=color.orange,axis=vector(0,0,1))
    
    xdot = box(width=1, length=2, height=0.5, opacity=0.8, pos=vector(0,0,0))
    
    for device in xdpcHandler.connectedDots():
        # Retrieve a packet
        device.resetOrientation(movelladot_pc_sdk.XRM_Heading)
        print("Orientation resetting")
    while(True):
        for device in xdpcHandler.connectedDots():
            packet = xdpcHandler.getNextPacket(device.portInfo().bluetoothAddress())
            if packet != None:
                if packet.containsOrientation():
                    quat = packet.orientationQuaternion()
                    roll, pitch, yaw = funcs.xDot.qToOri(quat[0], quat[1], quat[2], quat[3])
                    
                    rate(60)
                    k=vector(cos(yaw)*cos(pitch), sin(pitch),sin(yaw)*cos(pitch))
                    y=vector(0,1,0)
                    s=cross(k,y)
                    v=cross(s,k)
                    vrot=v*cos(roll)+cross(k,v)*sin(roll)
                    
                    frontArrow.axis=k
                    sideArrow.axis=cross(k,vrot)
                    upArrow.axis=vrot
                    xdot.axis=k
                    xdot.up=vrot
    
                    sideArrow.length=1
                    frontArrow.length=1
                    upArrow.length=1
                    
                    k = keysdown()
                    
                    if "r" in k:
                        device.resetOrientation(movelladot_pc_sdk.XRM_Heading)
                        print("Orientation resetting")
                    
                    if "esc" in k:
                        print("Disconnecting..")
                        xdpcHandler.cleanup()
                        exit(-1)
                        