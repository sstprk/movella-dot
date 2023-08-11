from vpython import *
from funcs import xDot
import asyncio

tools = xDot("C:\\Users\\Salih\Desktop\\Data\\left-upper-leg_D422CD037F_20210622_173151.xlsx")

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

roll, pitch, yaw = tools.qToeu()


for i in range(len(yaw)):
    rate(60)
    k=vector(cos(yaw[i])*cos(pitch[i]), sin(pitch[i]),sin(yaw[i])*cos(pitch[i]))
    y=vector(0,1,0)
    s=cross(k,y)
    v=cross(s,k)
    vrot=v*cos(roll[i])+cross(k,v)*sin(roll[i])
 
    frontArrow.axis=k
    sideArrow.axis=cross(k,vrot)
    upArrow.axis=vrot
    xdot.axis=k
    xdot.up=vrot
    
    sideArrow.length=1
    frontArrow.length=1
    upArrow.length=1


