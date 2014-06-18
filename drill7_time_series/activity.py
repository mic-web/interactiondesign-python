# -*- coding: utf-8 -*-
from pyqtgraph.flowchart import Flowchart
from pyqtgraph.flowchart.library.common import Node
import pyqtgraph.flowchart.library as fclib
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import sys
import time


def main():
    app = QtGui.QApplication(sys.argv)
    demo = Demo()
    demo.show()

    while True:
        demo.update()
        time.sleep(0.20)

    sys.exit(app.exec_())


class ActivityNode(Node):
    nodeName = "ActivityNode"

    def __init__(self, name):
        terminals = {
            'accelX': dict(io='in'),
            'accelY': dict(io='in'),
            'accelZ': dict(io='in'),
            'activity': dict(io='out'),
        }

        Node.__init__(self, name, terminals=terminals)

    def process(self, accelX, accelY, accelZ):
        data_x_length = len(accelX)
        data_y_length = len(accelY)
        data_z_length = len(accelZ)

        frequency_spectrum_x = np.fft.fft(accelX) / data_x_length
        frequency_spectrum_x = frequency_spectrum_x[range(data_x_length / 2)]
        frequency_spectrum_y = np.fft.fft(accelY) / data_y_length
        frequency_spectrum_y = frequency_spectrum_y[range(data_y_length / 2)]
        frequency_spectrum_z = np.fft.fft(accelZ) / data_z_length
        frequency_spectrum_z = frequency_spectrum_z[range(data_z_length / 2)]
        """
        frequency_spectrum = np.fft.fft(dataIn) / data_length
            # fft computing and normalization
        frequency_spectrum = frequency_spectrum[range(data_length / 2)]

        output =  np.abs(frequency_spectrum)
        """

        output = 'No activity yet...'
        return {'activity': output}

fclib.registerNodeType(ActivityNode, [('Data',)])


class Demo(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Demo, self).__init__()

        self.setWindowTitle("Wiimote Activity")
        self.showFullScreen()

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)

        fc = Flowchart(terminals={
            'dataIn': {'io': 'in'},
            'dataOut': {'io': 'out'}
        })

        self.layout.addWidget(fc.widget(), 0, 0, 4, 1)

        pwX = pg.PlotWidget()
        pwY = pg.PlotWidget()
        pwZ = pg.PlotWidget()
        pwX.getPlotItem().hideAxis('bottom')
        pwY.getPlotItem().hideAxis('bottom')
        pwZ.getPlotItem().hideAxis('bottom')

        self.label = QtGui.QLabel()
        self.label.setText("No activity yet...")
        font = QtGui.QFont("Arial")
        font.setPointSize(32)
        self.label.setFont(font)

        self.layout.addWidget(pwX, 0, 1)
        self.layout.addWidget(pwY, 1, 1)
        self.layout.addWidget(pwZ, 2, 1)
        self.layout.addWidget(self.label, 3, 1)

        sampling_rate = 150.0
        sampling_interval = 1.0 / sampling_rate  # Abtastfrequenz f = (1/t)
        time_vector = np.arange(0, 1, sampling_interval)
        signal_frequency = 10
        data = np.sin(2 * np.pi * signal_frequency * time_vector)
        fc.setInput(dataIn=data)

        pwXNode = fc.createNode('PlotWidget', pos=(-150, -150))
        pwXNode.setPlot(pwX)

        pwYNode = fc.createNode('PlotWidget', pos=(0, -150))
        pwYNode.setPlot(pwY)

        pwZNode = fc.createNode('PlotWidget', pos=(150, -150))
        pwZNode.setPlot(pwZ)

        self.activityNode = fc.createNode('ActivityNode', pos=(0, 150))

        # Einkommentieren falls mit Wii gearbeitet wird
        """
        wiimoteNode = fc.createNode('Wiimote', pos=(-300, 0))
        bufferXNode = fc.createNode('Buffer', pos=(-150, 0))
        bufferYNode = fc.createNode('Buffer', pos=(0, 0))
        bufferZNode = fc.createNode('Buffer', pos=(150, 0))
        """

        # Auskommentieren falls mit Wii gearbeitet wird
        fc.connectTerminals(fc['dataIn'], pwXNode['In'])
        fc.connectTerminals(fc['dataIn'], pwYNode['In'])
        fc.connectTerminals(fc['dataIn'], pwZNode['In'])
        fc.connectTerminals(fc['dataIn'], self.activityNode['accelX'])
        fc.connectTerminals(fc['dataIn'], self.activityNode['accelY'])
        fc.connectTerminals(fc['dataIn'], self.activityNode['accelZ'])

        # Einkommentieren falls mit Wii gearbeitet wird
        """
        fc.connectTerminals(wiimoteNode['accelX'], bufferXNode['dataIn'])
        fc.connectTerminals(wiimoteNode['accelY'], bufferYNode['dataIn'])
        fc.connectTerminals(wiimoteNode['accelZ'], bufferZNode['dataIn'])
        fc.connectTerminals(bufferXNode['dataOut'], pwXNode['In'])
        fc.connectTerminals(bufferYNode['dataOut'], pwYNode['In'])
        fc.connectTerminals(bufferZNode['dataOut'], pwZNode['In'])
        fc.connectTerminals(bufferXNode['dataOut'], activityNode['accelX'])
        fc.connectTerminals(bufferYNode['dataOut'], activityNode['accelY'])
        fc.connectTerminals(bufferZNode['dataOut'], activityNode['accelZ'])
        """

    def update(self):
        outputValues = self.activityNode.outputValues()
        self.label.setText(outputValues['activity'])
        pg.QtGui.QApplication.processEvents()

    def keyPressEvent(self, ev):
        if ev.key() == QtCore.Qt.Key_Escape:
            self.close()

if __name__ == '__main__':
    main()
