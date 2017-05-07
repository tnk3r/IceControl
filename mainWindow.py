#!/usr/bin/python
import serial, os, sys, platform
from PyQt4 import QtGui
from PyQt4.QtCore import QThread, pyqtSignal

class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        os.chdir(str(os.path.dirname(os.path.abspath(sys.argv[0]))))
        os.chdir("..")
        self.setFixedSize(800, 700)
        self.setStyleSheet("background-color: black;")
        self.styles = styles()

        self.slider1 = QtGui.QSlider(1, self)
        self.slider2 = QtGui.QSlider(1, self)
        self.slider3 = QtGui.QSlider(1, self)
        self.slider4 = QtGui.QSlider(1, self)
        self.slider5 = QtGui.QSlider(1, self)
        self.slider6 = QtGui.QSlider(1, self)
        self.speed1 = QtGui.QLabel("100%", self)
        self.speed2 = QtGui.QLabel("100%", self)
        self.speed3 = QtGui.QLabel("100%", self)
        self.speed4 = QtGui.QLabel("100%", self)
        self.speed5 = QtGui.QLabel("100%", self)
        self.speed6 = QtGui.QLabel("100%", self)

        self.sliderList = [self.slider1, self.slider2, self.slider3, self.slider4, self.slider5, self.slider6]
        self.speedList = [self.speed1, self.speed2, self.speed3, self.speed4, self.speed5, self.speed6]

        label_Y = 20
        for label in self.speedList:
            label.setStyleSheet("color: white;")
            label.move(560, label_Y)
            label_Y+=100

        x, y = 40, 20
        for slider in self.sliderList:
            slider.setFixedSize(500, 60)
            slider.setStyleSheet(self.styles.stylesheet())
            slider.setMinimum(100)
            slider.setMaximum(255)
            slider.move(x, y)
            slider.setValue(255)
            y+=100

        self.label = QtGui.QLabel("", self)
        self.label.setFixedSize(20, 20)
        self.label.move(30, 650)

        self.status_label = QtGui.QLabel("", self)
        self.status_label.setStyleSheet("color: white;")
        self.status_label.setFixedSize(200, 30)
        self.status_label.move(60, 655)

        # self.label.setText(os.getcwd()) # For debugging // May not need

        self.usbThread = usbThread(self)
        self.usbThread.start()

        self.slider1.sliderReleased.connect(self.setSlider1)
        self.slider2.sliderReleased.connect(self.setSlider2)
        self.slider3.sliderReleased.connect(self.setSlider3)
        self.slider4.sliderReleased.connect(self.setSlider4)
        self.slider5.sliderReleased.connect(self.setSlider5)
        self.slider6.sliderReleased.connect(self.setSlider6)

        self.usbThread.status.connect(self.label.setStyleSheet)
        self.usbThread.status_message.connect(self.status_label.setText)
        self.show()
        self.raise_()

    def setSlider1(self):
        self.usbThread.sendCommand("1"+str(self.slider1.value()))
        self.speed1.setText(str(int(self.slider1.value() *.3952))+"%")

    def setSlider2(self):
        self.usbThread.sendCommand("2"+str(self.slider2.value()))
        self.speed2.setText(str(int(self.slider2.value()*.3952))+"%")

    def setSlider3(self):
        self.usbThread.sendCommand("3"+str(self.slider3.value()))
        self.speed3.setText(str(int(self.slider3.value()*.3952))+"%")

    def setSlider4(self):
        self.usbThread.sendCommand("4"+str(self.slider4.value()))
        self.speed4.setText(str(int(self.slider4.value()*.3952))+"%")

    def setSlider5(self):
        self.usbThread.sendCommand("5"+str(self.slider5.value()))
        self.speed5.setText(str(int(self.slider5.value()*.3952))+"%")

    def setSlider6(self):
        self.usbThread.sendCommand("6"+str(self.slider6.value()))
        self.speed6.setText(str(int(self.slider6.value()*.3952))+"%")


class usbThread(QThread):

    temp1 = pyqtSignal(str)
    status = pyqtSignal(str)
    status_message = pyqtSignal(str)

    def __init__(self, parent):
        QThread.__init__(self, parent=None)
        self.name = "NanoThread"
        self.board_connected = 0
        serial_address = ""
        if platform.system() == "Linux":
            try:
                for device in os.listdir('/dev/'):
                    if "ttyUSB" in device:
                        serial_address = "/dev/"+str(device)
                        self.board_connected = 1
                        self.status.emit("background-color: green;")
            except StandardError as msg:
                self.status.emit("background-color: red;")

        if platform.system() == "Darwin":
            try:
                for device in os.listdir('/dev/'):
                    if "wchusbserial" in device:
                        serial_address = "/dev/"+str(device)
                        self.board_connected = 1
                        self.status.emit("background-color: green;")
            except StandardError as msg:
                self.status.emit("background-color: red;")

        if serial_address != "":
            self.serial = serial.Serial(serial_address, 9600)

    def run(self):
        while int(self.board_connected) == 1:
            self.parseData()
            self.status.emit("background-color: lime; border-radius: 5;")

    def parseData(self):
        data = self.serial.read_until("\n")
        if "rv" in data:
            self.status_message.emit(str(data))
        print data

    def sendCommand(self, command):
        if len(command) <= 4:
            self.serial.write(str(command))

class styles():

    def __init__(self):
        self.styles_imported = 1

    def stylesheet(self):
        return """
                QSlider::groove:horizontal {
                    height: 50px;
                    border: 0px solid #abc;
                    }
                QSlider::sub-page:horizontal {
                    background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,
                        stop: 0 #333, stop: 1 #aaa);
                    background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,
                        stop: 0 #333, stop: 1 #aaa);
                    height: 40px;
                }
                QSlider::add-page:horizontal {
                    background: #222;
                    border: 2px solid gray;
                    height: 40px;
                }
                QSlider::handle:horizontal {
                    background: #000;
                    width: 35px;
                    border: 2px solid white;
                    margin-top: 0px;
                    margin-bottom: 0px;
                    border-radius: 0px;
                }
            """

    def buttonstyle(self):
        return """
                QPushButton {
                    color: white;
                    background-color: rgb(50, 50, 50);
                    border-style: solid;
                    border-width: 2px;
                    border-radius: 5px;
                    border-color: white;
                    font: bold 35px;
                    font-style: italic;
                }
                QPushButton::pressed {
                    background-color: rgb(200, 200, 200);
                    border-style: inset;
                }
            """

app = QtGui.QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())
