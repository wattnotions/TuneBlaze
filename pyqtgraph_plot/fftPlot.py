#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Update a simple plot as rapidly as possible to measure speed.
"""

## Add path to library (just for examples; you do not need this)
import initExample
import serial
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time

ser = serial.Serial(
    port='COM6',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=None
)

ser.close()
ser.open()
print (ser.isOpen())

app = QtGui.QApplication([])

p = pg.plot()
p.setLogMode(False, True)
p.setWindowTitle('pyqtgraph example: PlotSpeedTest')
#p.setRange(QtCore.QRectF(0, -10, 5000, 20)) 
p.setLabel('bottom', 'Index', units='B')
p.setYRange(0, 6000, padding=0)

#p.setXRange(0,300)
curve = p.plot()

#curve.setFillBrush((0, 0, 100, 100))
#curve.setFillLevel(0)

#lr = pg.LinearRegionItem([100, 4900])
#p.addItem(lr)

#data = np.random.normal(size=(50,5000))
ptr = 0
lastTime = time()
fps = None
def update():
    global curve, data, ptr, p, lastTime, fps
    
    byte = str(ser.readline().strip())
    #print(byte)
    
    try:
        if (byte[2] == '*'):
        
            data = (ser.readline().strip())
            #print("printing dat...")
            #print(data)
            #print(data[2])
            
            
            split_data = data.decode('ascii').split(',')
            #print(split_data)
            split_data = list(map(float, split_data[:-1]))
            
            
            curve.setData((split_data))
    except:
       pass
        
    
    ptr += 1
    now = time()
    dt = now - lastTime
    lastTime = now
    if fps is None:
        fps = 1.0/dt
    else:
        s = np.clip(dt*3., 0, 1)
        fps = fps * (1-s) + (1.0/dt) * s
    p.setTitle('%0.2f fps' % fps)
    app.processEvents()  ## force complete redraw for every plot
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)
    


## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
