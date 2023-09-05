from vpython import *
from xdpchandler import *
import funcs


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
        filterProfiles = device.getAvailableFilterProfiles()
        print("Available filter profiles:")
        for f in filterProfiles:
            print(f.label())

        print(f"Current profile: {device.onboardFilterProfile().label()}")
        if device.setOnboardFilterProfile("General"):
            print("Successfully set profile to General")
        else:
            print("Setting filter profile failed!")

        print("Setting quaternion CSV output")
        device.setLogOptions(movelladot_pc_sdk.XsLogOptions_Quaternion)

        logFileName = "logfile_" + device.bluetoothAddress().replace(':', '-') + ".csv"
        print(f"Enable logging to: {logFileName}")
        if not device.enableLogging(logFileName):
            print(f"Failed to enable logging. Reason: {device.lastResultText()}")

        print("Putting device into measurement mode.")
        if not device.startMeasurement(movelladot_pc_sdk.XsPayloadMode_OrientationQuaternion):
            print(f"Could not put device into measurement mode. Reason: {device.lastResultText()}")
            continue

if device.startMeasurement(movelladot_pc_sdk.XsPayloadMode_OrientationQuaternion):
    scene.range = 5
    scene.background = color.white
    
    scene.width = 950
    scene.height = 700
    
    xarrow = arrow(length=10, shaftwidth=.01, color=color.green, axis=vector(1,0,0))
    yarrow = arrow(length=10, shaftwidth=.01, color=color.red, axis=vector(0,1,0))
    zarrow = arrow(length=10, shaftwidth=.01, color=color.blue, axis=vector(0,0,1))
    
    frontArrow=arrow(length=4,shaftwidth=.05,color=color.purple,axis=vector(1,0,0))
    upArrow=arrow(length=1,shaftwidth=.05,color=color.magenta,axis=vector(0,1,0))
    sideArrow=arrow(length=2,shaftwidth=.05,color=color.orange,axis=vector(0,0,1))
    
    xdot = box(width=1, length=1, height=0.5, opacity=0.8, pos=vector(0,0,0))
    
    for device in xdpcHandler.connectedDots():
        # Retrieve a packet
        device.resetOrientation(movelladot_pc_sdk.XRM_Heading)
        print("Orientation resetting")
        
    while True:
        for device in xdpcHandler.connectedDots():
            packet = xdpcHandler.getNextPacket(device.portInfo().bluetoothAddress())
            if packet != None:
                if packet.containsOrientation():
                    quat = packet.orientationQuaternion()
                    roll, pitch, yaw = funcs.xDot.qToeu(quat[0], quat[1], quat[2], quat[3])
        """if not orientationResetDone and (movelladot_pc_sdk.XsTimeStamp_nowMs() - startTime) % 5000 == 0:
            for device in xdpcHandler.connectedDots():
                print(f"\nResetting heading for device {device.portInfo().bluetoothAddress()}: ", end="", flush=True)
                if device.resetOrientation(movelladot_pc_sdk.XRM_Heading):
                    print("OK", end="", flush=True)
                else:
                    print(f"NOK: {device.lastResultText()}", end="", flush=True)
            print("\n", end="", flush=True)"""
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
    
