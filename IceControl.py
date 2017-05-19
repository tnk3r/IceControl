#!/usr/bin/python

import serial, os, sys, platform, time
from PyQt4 import QtGui
from PyQt4.QtCore import QThread, pyqtSignal

class aboutWindow(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setFixedSize(400, 150)
        self.move(600, 300)
        self.defaultText = "\tIceControl Version .45\n\n\t  tink3r (AlexCarr)"

        self.textLabel = QtGui.QLabel(self.defaultText, self)
        self.textLabel.move(85, 30)

        self.okButton = QtGui.QPushButton("OK", self)
        self.okButton.move(140, 100)
        self.okButton.setFixedSize(100, 40)
        self.okButton.clicked.connect(self.close)

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

class Window(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        os.chdir(str(os.path.dirname(os.path.abspath(sys.argv[0]))))
        os.chdir("..")
        self.setFixedSize(650, 700)
        self.setStyleSheet("background-color: black; border-color: white")
        self.setWindowTitle("IceBoard Fan Controller")
        self.styles = styles()
        self.setWindowTitle("IceControl")

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
        self.speed1 = QtGui.QLabel("100%", self)
        self.speed2 = QtGui.QLabel("100%", self)
        self.speed3 = QtGui.QLabel("100%", self)
        self.speed4 = QtGui.QLabel("100%", self)
        self.speed5 = QtGui.QLabel("100%", self)
        self.speed6 = QtGui.QLabel("100%", self)

        self.chan1 = QtGui.QLabel("Channel 1", self)
        self.chan2 = QtGui.QLabel("Channel 2", self)
        self.chan3 = QtGui.QLabel("Channel 3", self)
        self.chan4 = QtGui.QLabel("Channel 4", self)
        self.chan5 = QtGui.QLabel("Channel 5", self)
        self.chan6 = QtGui.QLabel("Channel 6", self)

        self.sliderList = [self.slider1, self.slider2, self.slider3, self.slider4, self.slider5, self.slider6]
        self.speedList = [self.speed1, self.speed2, self.speed3, self.speed4, self.speed5, self.speed6]
        self.chanList = [self.chan1, self.chan2, self.chan3, self.chan4, self.chan5, self.chan6]
        chanY = 50
        for channel in self.chanList:
            channel.setStyleSheet("color: white; font-size 20px;")
            channel.move(30, chanY)
            chanY+=100
        label_Y = 100
        for label in self.speedList:
            label.setStyleSheet("color: white; font-size: 25px; font-style: italic")
            label.move(560, label_Y)
            label_Y+=100

        x, y = 40, 80
        for slider in self.sliderList:
            slider.setFixedSize(500, 60)
            slider.setStyleSheet(self.styles.stylesheet())
            slider.setMinimum(100)
            slider.setMaximum(255)
            slider.move(x, y)
            slider.setValue(255)
            y+=100

        self.titlelabel = QtGui.QLabel("IceBoard Fan Controller", self)
        self.titlelabel.setFixedSize(300, 40)
        self.titlelabel.move(20, 10)
        self.titlelabel.setStyleSheet("font-size: 25px; color: white; font-style: italic;")

        self.label = QtGui.QLabel("", self)
        self.label.setFixedSize(20, 20)
        self.label.setStyleSheet("background-color: red; border-radius: 8px;")
        self.label.move(30, 650)

        self.status_label = QtGui.QLabel("IceBoard Disconnected", self)
        self.status_label.setStyleSheet("color: white;")
        self.status_label.setFixedSize(200, 30)
        self.status_label.move(60, 650)

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


        self.show()
        self.raise_()

    def openAbout(self):
        self.utilWindow.move(self.geometry().x() + 100, self.geometry().y() + 20)
        self.utilWindow.open()

    def openAlert(self, message):
        self.utilWindow.move(self.geometry().x() + 100, self.geometry().y() + 20)
        self.utilWindow.alert(str(message))

    def setSlider1(self):
        try:
            self.usbThread.sendCommand("1"+str(self.slider1.value()))
            self.speed1.setText(str(int(self.slider1.value() *.3952))+"%")
        except StandardError as msg:
            self.openAlert("NO IceBoard Found!")

    def setSlider2(self):
        try:
            self.usbThread.sendCommand("2"+str(self.slider2.value()))
            self.speed2.setText(str(int(self.slider2.value()*.3952))+"%")
        except StandardError as msg:
            self.openAlert("NO IceBoard Found!")

    def setSlider3(self):
        try:
            self.usbThread.sendCommand("3"+str(self.slider3.value()))
            self.speed3.setText(str(int(self.slider3.value()*.3952))+"%")
        except StandardError as msg:
            self.openAlert("NO IceBoard Found!")

    def setSlider4(self):
        try:
            self.usbThread.sendCommand("4"+str(self.slider4.value()))
            self.speed4.setText(str(int(self.slider4.value()*.3952))+"%")
        except StandardError as msg:
            self.openAlert("NO IceBoard Found!")

    def setSlider5(self):
        try:
            self.usbThread.sendCommand("5"+str(self.slider5.value()))
            self.speed5.setText(str(int(self.slider5.value()*.3952))+"%")
        except StandardError as msg:
            self.openAlert("NO IceBoard Found!")

    def setSlider6(self):
        try:
            self.usbThread.sendCommand("6"+str(self.slider6.value()))
            self.speed6.setText(str(int(self.slider6.value()*.3952))+"%")
        except StandardError as msg:
            self.openAlert("NO IceBoard Found!")


class usbThread(QThread):

    temp1 = pyqtSignal(str)
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

    def __init__(self, parent):
        QThread.__init__(self, parent=None)
        self.name = "NanoThread"
        self.board_connected = 0
        serial_address = ""
        self.sliderSignals = [self.slider1, self.slider2, self.slider3, self.slider4, self.slider5, self.slider6]
        self.values = [self.value1, self.value2, self.value3, self.value4, self.value5, self.value6]

    def serial_setup(self):
        #need to test on Windows 10
        if platform.system() == "Cygwin":
            self.status_message.emit("No Ice Board Connected")

        if platform.system() == "Linux":
            try:
                # better Linux Detection
                for device in os.listdir('/dev/'):
                    if "ttyUSB" in device:
                        serial_address = "/dev/"+str(device)
                        self.board_connected = 1
                        self.status.emit("background-color: lime; border-radius: 8px;")
            except StandardError as msg:
                self.status.emit("background-color: red; border-radius: 8px;")
                self.status_message.emit("No Ice Board Connected")

        if platform.system() == "Darwin":
            x = 0
            try:
                # hopefully nobody connects a bunch of chinese nanos together.
                for device in os.listdir('/dev/'):
                    if "wchusbserial" in device:
                        serial_address = "/dev/"+str(device)
                        self.board_connected = 1
                        x +=1
                if x > 0:
                    self.status.emit("background-color: lime; border-radius: 8px;")

            except StandardError as msg:
                print "no iceboard :("

        try:
            if serial_address != "":
                self.serial = serial.Serial(serial_address, 9600)
        except StandardError as msg:
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
            time.sleep(0.3)

    def parseData(self):
        data = self.serial.read_until("\n").strip()
        if "rv" in data:
            self.status_message.emit(str(data).strip()+": Connected! ")
        if len(data) == 4:
            print "Channel: "+str(data)[0]+" set at "+str(data)[1:4]
            print int(str(data)[0]) - 1
            self.sliderSignals[int(str(data)[0]) - 1].emit(int(str(data)[1:4]))
            self.values[int(str(data)[0]) - 1].emit(str(int(round(int(str(data)[1:4])*.394)))+"%")

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
                    width: 20px;
                    border: 2px solid white;
                    margin-top: 0px;
                    margin-bottom: 0px;
                    border-radius: 8px;
                }
            """

    def buttonstyle(self, size, color):
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
app = QtGui.QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())
