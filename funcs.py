import math as m
from xdpchandler import *
import movelladot_pc_sdk
from numpy import dot, sum, tile, linalg
from numpy.linalg import inv

class xDot:
    @staticmethod
    def qToOri(q0, q1, q2, q3):
        roll=m.atan2(2*(q0*q1+q2*q3),1-2*(q1*q1+q2*q2))
        pitch=-m.asin(2*(q0*q2-q3*q1))
        yaw=-m.atan2(2*(q0*q3+q1*q2),1-2*(q2*q2+q3*q3))-m.pi/2
        return roll, pitch, yaw
    
    @staticmethod
    def kf_predict(X, P, A, Q, B, U):
        X = dot(A, X) + dot(B, U)
        P = dot(A, dot(P, A.T)) + Q
        return(X,P) 
    
    @classmethod
    def kf_update(cls, X, P, Y, H, R):
         IM = dot(H, X)
         IS = R + dot(H, dot(P, H.T))
         K = dot(P, dot(H.T, inv(IS)))
         X = X + dot(K, (Y-IM))
         P = P - dot(K, dot(IS, K.T))
         LH = cls.gauss_pdf(Y, IM, IS)
         return (X,P,K,IM,IS,LH)
     
    @staticmethod
    def gauss_pdf(X, M, S):
        if M.shape()[1] == 1:
             DX = X - tile(M, X.shape()[1])
             E = 0.5 * sum(DX * (dot(inv(S), DX)), axis=0)
             E = E + 0.5 * M.shape()[0] * m.log(2 * m.pi) + 0.5 * m.log(m.det(S))
             P = m.exp(-E)
        elif X.shape()[1] == 1:
             DX = tile(X, M.shape()[1])- M
             E = 0.5 * sum(DX * (dot(inv(S), DX)), axis=0)
             E = E + 0.5 * M.shape()[0] * m.log(2 * m.pi) + 0.5 * m.log(m.det(S))
             P = m.exp(-E)
        else:
             DX = X-M
             E = 0.5 * dot(DX.T, dot(inv(S), DX))
             E = E + 0.5 * M.shape()[0] * m.log(2 * m.pi) + 0.5 * m.log(m.det(S))
             P = m.exp(-E)
        return (P[0],E[0])