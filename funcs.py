import pandas as pd
import math as m
from bleak import BleakScanner
import asyncio
import xlsxwriter

class xDot:
    def __init__(self, path):
        self.path = path
        self.df = pd.DataFrame(pd.read_excel(path))
        self.devices = []

    def qToeu(self):
        roll = []
        pitch = []
        yaw = []
        for x in range(len(self.df.loc[:,"Quat_W"])): 
            q0 = float(self.df.loc[x,"Quat_W"])
            q1 = float(self.df.loc[x,"Quat_X"])
            q2 = float(self.df.loc[x,"Quat_Y"])
            q3 = float(self.df.loc[x,"Quat_Z"])
                
            roll.append(-m.atan2(2*(q0*q1+q2*q3), 1-2*(q1*q1+q2*q2)))
            pitch.append((-m.pi/2)+2*m.atan2(m.sqrt(1+2*(q0*q2-q3*q1)), m.sqrt(1-2*(q0*q2-q3*q1))))
            yaw.append(-m.atan2(2*(q0*q3+q1*q2), 1-2*(q2*q2+q3*q3)))
                
        return roll, pitch, yaw
    
    async def scanner(self):
        async with BleakScanner() as scanner:
            self.devices = await scanner.discover()
            for dev in self.devices:
                print(dev)

    def writeData(self):
        workbook = xlsxwriter.Workbook("Data.xlsx")
        sheet = workbook.add_worksheet("Data")

        for x in range(len(self.df.loc[:,"Quat_W"])): 
            q0 = float(self.df.loc[x,"Quat_W"])
            sheet.write(1, x, q0)
            q1 = float(self.df.loc[x,"Quat_X"])
            sheet.write(2, x, q1)
            q2 = float(self.df.loc[x,"Quat_Y"])
            sheet.write(3, x, q2)
            q3 = float(self.df.loc[x,"Quat_Z"])
            sheet.write(4, x, q3)
        workbook.close()