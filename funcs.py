import math as m

class xDot:
    def __init__(self, path):
        pass

    def qToeu(q0, q1, q2, q3):
        roll = (m.atan2(2*(q0*q1+q2*q3), 1-2*(q1*q1+q2*q2)))
        pitch = ((m.pi/2)+2*m.atan2(m.sqrt(1+2*(q0*q2-q3*q1)), m.sqrt(1-2*(q0*q2-q3*q1))))
        yaw = (m.atan2(2*(q0*q3+q1*q2), 1-2*(q2*q2+q3*q3)))
        return roll, pitch, yaw
    
