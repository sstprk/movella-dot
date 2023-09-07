import math as m
from xdpchandler import *
import movelladot_pc_sdk
class xDot:
    def qToOri(q0, q1, q2, q3):
        roll=-m.atan2(2*(q0*q1+q2*q3),1-2*(q1*q1+q2*q2))
        pitch=m.asin(2*(q0*q2-q3*q1))
        yaw=-m.atan2(2*(q0*q3+q1*q2),1-2*(q2*q2+q3*q3))-m.pi/2
        return roll, pitch, yaw