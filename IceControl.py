#!/usr/bin/python

import serial, os, sys, platform, time
from PyQt4 import QtGui
from PyQt4.QtCore import QThread, pyqtSignal

def slider_style():
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
                    width: 20px;
                    border: 2px solid white;
                    margin-top: 0px;
                    margin-bottom: 0px;
                    border-radius: 8px;
                }
            """

def buttonstyle(size, color):

    return """
                QPushButton {
                    color:"""+str(color)+""";
                    background-color: rgb(50, 50, 50);
                    border-style: solid;
                    border-width: 2px;
                    border-radius: 5px;
                    border-color: white;
                    font:"""+str(size)+"""px;
                    font-style: italic;
                }
                QPushButton::pressed {
                    background-color: rgb(200, 200, 200);
                    border-style: inset;
                }
            """

def labelstyle(size, color):
    return """
                QLabel {
                    color:"""+str(color)+""";
                    background-color: rgb(0, 0, 0);
                    font:"""+str(size)+"""px;
                }
            """

class customQPushButton(QtGui.QPushButton):

    def __init__(self, string, parent, x_move, y_move, x_size=100, y_size=40, stylesheet=buttonstyle(25, "white"), function=""):
        QtGui.QPushButton.__init__(self, parent=parent)
        self.setText(string)
        self.setFixedSize(x_size, y_size)
        self.move(x_move, y_move)
        self.setStyleSheet(stylesheet)
        if function != "": self.clicked.connect(function)

class customQLabel(QtGui.QLabel):

    def __init__(self, string, parent, x_move, y_move, x_size=80, y_size=30, stylesheet=labelstyle(25, "white")):
        QtGui.QLabel.__init__(self, parent=parent)
        self.setText(string)
        self.setFixedSize(x_size, y_size)
        self.move(x_move, y_move)
        self.setStyleSheet(stylesheet)


class aboutWindow(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setFixedSize(400, 150)
        self.move(600, 300)
        self.setStyleSheet("background-color: black; border-color: 5 px solid white")
        self.defaultText = "\tIceControl Version .75\n\n\t  tink3r (AlexCarr)"
        self.textLabel = customQLabel(self.defaultText, self, 85, 30, stylesheet=labelstyle(20, "white"))
        self.okButton = customQPushButton("OK", self, 140, 100, 100, 40, buttonstyle(25, "white"), self.close)

    def open(self):
        self.textLabel.setText(self.defaultText)
        self.show()
        self.raise_()

    def close(self):
        self.hide()

    def alert(self, message):
        self.textLabel.setText(str(message))
        self.show()
        self.raise_()
        time.sleep(2)
        self.hide()

class Window(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        os.chdir(str(os.path.dirname(os.path.abspath(sys.argv[0]))))
        os.chdir("..")
        self.setFixedSize(650, 700)
        self.setStyleSheet("background-color: black; border-color: 5 px solid white")
        self.setWindowTitle("IceBoard Fan Controller")
        self.setWindowTitle("IceControl")
        x, y = 40, 80
        chanY, label_Y = 50, 100

        self.utilWindow = aboutWindow()

        exitAction = QtGui.QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(app.quit)
        aboutAction = QtGui.QAction('About...', self)
        aboutAction.triggered.connect(self.openAbout)

        self.menubar = self.menuBar()
        self.file_menu = self.menubar.addMenu("&File")
        self.file_menu.addAction(exitAction)
        self.file_menu.addAction(aboutAction)

        self.slider1 = QtGui.QSlider(1, self)
        self.slider2 = QtGui.QSlider(1, self)
        self.slider3 = QtGui.QSlider(1, self)
        self.slider4 = QtGui.QSlider(1, self)
        self.slider5 = QtGui.QSlider(1, self)
        self.slider6 = QtGui.QSlider(1, self)
        self.speed1 = customQLabel("100%", self, 560, label_Y)
        self.speed2 = customQLabel("100%", self, 560, label_Y+100)
        self.speed3 = customQLabel("100%", self, 560, label_Y+200)
        self.speed4 = customQLabel("100%", self, 560, label_Y+300)
        self.speed5 = customQLabel("100%", self, 560, label_Y+400)
        self.speed6 = customQLabel("100%", self, 560, label_Y+500)
        self.chan1 = customQLabel("Channel 1", self, 30, chanY, stylesheet="color: white; font-size 20px;")
        self.chan2 = customQLabel("Channel 2", self, 30, chanY+100, stylesheet="color: white; font-size 20px;")
        self.chan3 = customQLabel("Channel 3", self, 30, chanY+200, stylesheet="color: white; font-size 20px;")
        self.chan4 = customQLabel("Channel 4", self, 30, chanY+300, stylesheet="color: white; font-size 20px;")
        self.chan5 = customQLabel("Channel 5", self, 30, chanY+400, stylesheet="color: white; font-size 20px;")
        self.chan6 = customQLabel("Channel 6", self, 30, chanY+500, stylesheet="color: white; font-size 20px;")

        self.sliderList = [self.slider1, self.slider2, self.slider3, self.slider4, self.slider5, self.slider6]
        self.speedList = [self.speed1, self.speed2, self.speed3, self.speed4, self.speed5, self.speed6]
        self.chanList = [self.chan1, self.chan2, self.chan3, self.chan4, self.chan5, self.chan6]

        for slider in self.sliderList:
            slider.setFixedSize(500, 60)
            slider.setStyleSheet(slider_style())
            slider.setMinimum(10)
            slider.setMaximum(255)
            slider.move(x, y)
            slider.setValue(255)
            y+=100

        self.usbThread = usbThread(self)

        self.tinklabel = customQLabel(".tink3r", self, 550, 670, stylesheet="font-size: 15px; color:rgb(50,50,50); font-style: italic;")
        self.setMaxButton = customQPushButton("setMAX", self, 130, 10, stylesheet=buttonstyle(20, "white"), function=self.setMaxOnAllChannels)
        self.setMinButton = customQPushButton("setMin", self, 20, 10, stylesheet=buttonstyle(20, "white"), function=self.setMinOnAllChannels)
        self.updateButton = customQPushButton("Update Firmware", self, 100, 20, stylesheet=buttonstyle(25, "white"), function=self.updateFirmware)
        self.temp1Label = customQLabel("TEMP1:", self, 380, 10, stylesheet=labelstyle(10, "white"))
        self.temp2Label = customQLabel("TEMP2:", self, 480, 10, stylesheet=labelstyle(10, "white"))
        self.temp3Label = customQLabel("TEMP3:", self, 580, 10, stylesheet=labelstyle(10, "white"))
        self.temp1ValueLabel = customQLabel("  ", self, 400, 40, stylesheet=labelstyle(25, "white"))
        self.temp2ValueLabel = customQLabel("  ", self, 500, 40, stylesheet=labelstyle(25, "white"))
        self.temp3ValueLabel = customQLabel("  ", self, 600, 40, stylesheet=labelstyle(25, "white"))
        self.label = customQLabel("", self, 30, 650, 20, 20, "background-color: red; border-radius: 8px;")
        self.status_label = customQLabel("IceBoard Disconnected", self, 60, 650, 200, 30, "color: white;")

        self.updateButton.hide()

        self.usbThread.start()

        self.slider1.sliderReleased.connect(self.setSlider1)
        self.slider2.sliderReleased.connect(self.setSlider2)
        self.slider3.sliderReleased.connect(self.setSlider3)
        self.slider4.sliderReleased.connect(self.setSlider4)
        self.slider5.sliderReleased.connect(self.setSlider5)
        self.slider6.sliderReleased.connect(self.setSlider6)

        self.usbThread.status.connect(self.label.setStyleSheet)
        self.usbThread.status_message.connect(self.status_label.setText)
        self.usbThread.status_message.connect(self.openAlert)
        self.usbThread.slider1.connect(self.slider1.setValue)
        self.usbThread.slider2.connect(self.slider2.setValue)
        self.usbThread.slider3.connect(self.slider3.setValue)
        self.usbThread.slider4.connect(self.slider4.setValue)
        self.usbThread.slider5.connect(self.slider5.setValue)
        self.usbThread.slider6.connect(self.slider6.setValue)
        self.usbThread.value1.connect(self.speed1.setText)
        self.usbThread.value2.connect(self.speed2.setText)
        self.usbThread.value3.connect(self.speed3.setText)
        self.usbThread.value4.connect(self.speed4.setText)
        self.usbThread.value5.connect(self.speed5.setText)
        self.usbThread.value6.connect(self.speed6.setText)
        self.usbThread.temp1.connect(self.temp1ValueLabel.setText)
        self.usbThread.temp2.connect(self.temp2ValueLabel.setText)
        self.usbThread.temp3.connect(self.temp3ValueLabel.setText)
        #self.usbThread.updateSignal.connect(self.showUpdateButton)
        self.show()
        self.raise_()

    def showUpdateButton(self):
        self.updateButton.show()
        self.updateButton.raise_()

    def openAbout(self):
        self.utilWindow.move(self.geometry().x() + 100, self.geometry().y() + 20)
        self.utilWindow.open()

    def openAlert(self, message):
        self.utilWindow.move(self.geometry().x() + 100, self.geometry().y() + 20)
        self.utilWindow.alert(str(message))

    def setSlider1(self):
        try:
            self.usbThread.sendCommand("1"+str(self.slider1.value()).zfill(3))
            self.speed1.setText(self.convertValueToSlider(self.slider1.value()))
        except StandardError as msg:
            self.openAlert("NO IceBoard Found!")

    def setSlider2(self):
        try:
            self.usbThread.sendCommand("2"+str(self.slider2.value()).zfill(3))
            self.speed2.setText(self.convertValueToSlider(self.slider2.value()))
        except StandardError as msg:
            self.openAlert("NO IceBoard Found!")

    def setSlider3(self):
        try:
            self.usbThread.sendCommand("3"+str(self.slider3.value()).zfill(3))
            self.speed3.setText(self.convertValueToSlider(self.slider3.value()))
        except StandardError as msg:
            self.openAlert("NO IceBoard Found!")

    def setSlider4(self):
        try:
            self.usbThread.sendCommand("4"+str(self.slider4.value()).zfill(3))
            self.speed4.setText(self.convertValueToSlider(self.slider4.value()))
        except StandardError as msg:
            self.openAlert("NO IceBoard Found!")

    def setSlider5(self):
        try:
            self.usbThread.sendCommand("5"+str(self.slider5.value()).zfill(3))
            self.speed5.setText(self.convertValueToSlider(self.slider5.value()))
        except StandardError as msg:
            self.openAlert("NO IceBoard Found!")

    def setSlider6(self):
        try:
            self.usbThread.sendCommand("6"+str(self.slider6.value()).zfill(3))
            self.speed6.setText(self.convertValueToSlider(self.slider6.value()))
        except StandardError as msg:
            self.openAlert("NO IceBoard Found!")

    def convertValueToSlider(self, value):
        calc = int(round(value * .3952))
        return str(calc)+"%"

    def setMaxOnAllChannels(self):
        self.usbThread.sendCommand("MAX\n")

    def setMinOnAllChannels(self):
        self.usbThread.sendCommand("MIN\n")

    def updateFirmware(self):
        print "Updating atmel"

class usbThread(QThread):

    temp1 = pyqtSignal(str)
    temp2 = pyqtSignal(str)
    temp3 = pyqtSignal(str)
    status = pyqtSignal(str)
    status_message = pyqtSignal(str)
    slider1 = pyqtSignal(int)
    slider2 = pyqtSignal(int)
    slider3 = pyqtSignal(int)
    slider4 = pyqtSignal(int)
    slider5 = pyqtSignal(int)
    slider6 = pyqtSignal(int)

    value1 = pyqtSignal(str)
    value2 = pyqtSignal(str)
    value3 = pyqtSignal(str)
    value4 = pyqtSignal(str)
    value5 = pyqtSignal(str)
    value6 = pyqtSignal(str)

    updateSignal = pyqtSignal()


    def __init__(self, parent):
        QThread.__init__(self, parent=None)
        self.name = "NanoThread"
        self.version = 180
        self.board_connected = 0
        self.sliderSignals = [self.slider1, self.slider2, self.slider3, self.slider4, self.slider5, self.slider6]
        self.values = [self.value1, self.value2, self.value3, self.value4, self.value5, self.value6]

    def serial_setup(self):
        #need to test on Windows 10
        if platform.system() == "Cygwin":
            self.status_message.emit("No Ice Board Connected")

        if platform.system() == "Linux":
            try:
                for device in os.listdir('/dev/'):
                    if "ttyUSB" in device:
                        serial_address = "/dev/"+str(device)
                        self.board_connected = 1
                        self.status.emit("background-color: lime; border-radius: 8px;")
            except StandardError as msg:
                self.status.emit("background-color: red; border-radius: 8px;")
                self.status_message.emit("No Ice Board Connected")
                print str(msg)

        if platform.system() == "Darwin":
            x = 0
            try:
                ### "hopefully nobody connects a bunch of chinese nanos together."
                for device in os.listdir('/dev/'):
                    if "wchusbserial" in device:
                        serial_address = "/dev/"+str(device)
                        self.board_connected = 1
                        x +=1
                if x > 0:
                    self.status.emit("background-color: lime; border-radius: 8px;")
            except StandardError as msg:
                print "no iceboard :("+str(msg)


        try:
            if serial_address != "":
                self.serial = serial.Serial(serial_address, 9600)
        except StandardError as msg:
            print str(msg)
            self.board_connected = 0
            self.status.emit("background-color: red; border-radius: 8px")
            self.status_message.emit("No Ice Board Connected")
            time.sleep(2)

    def run(self):
        while True:
            if int(self.board_connected) == 1:
                try:
                    self.parseData()
                    self.status.emit("background-color: lime; border-radius: 8;")
                except StandardError as msg:
                    print str(msg)
                    self.status.emit("background-color: red; border-radius: 8;")
                    self.status_message.emit("No Ice Board Connected")
                    self.board_connected = 0
            else:
                self.serial_setup()
            time.sleep(0.2)

    def parseData(self):
        data = self.serial.read_until("\n").strip()
        if "rv" in data:
            self.status_message.emit(str(data).strip()+": Connected! ")
            print str(data).split(":")[0].split("_")[2].replace("v", "")
            if int(str(data).split(":")[0].split("_")[2].replace("v", "")) < self.version:
                print "Updating"
                self.updateSignal.emit()

        if len(data) == 4:
            try:
                self.sliderSignals[int(str(data)[0]) - 1].emit(int(str(data)[1:4]))
                self.values[int(str(data)[0]) - 1].emit(str(int(round(int(data[1:4])*.394)))+"%")
            except StandardError as msg:
                print str(msg)
        if data[0:3] == "TMP":
            temp = data.split(":")
            if temp[1] != "0":
                self.temp1.emit(self.convertTemp(temp[1]))
            else:
                self.temp1.emit("-")
            if temp[2] != "0":
                self.temp2.emit(self.convertTemp(temp[2]))
            else:
                self.temp2.emit("-")
            if temp[3] != "0":
                self.temp3.emit(self.convertTemp(temp[3]))
            else:
                self.temp3.emit("-")

    def convertTemp(self, raw):
        celsius = ((int(raw) * 3000/1024) - 500) / 20
        return str(celsius)+"C"

    def sendCommand(self, command):
        if len(command) <= 4:
            self.serial.write(str(command)+"\n")


app = QtGui.QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())
