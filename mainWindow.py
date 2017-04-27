#!/usr/bin/python
import serial, os, sys
from PyQt4 import QtGui
from PyQt4.QtCore import QString, QThread, pyqtSignal

class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        os.chdir(str(os.path.dirname(os.path.abspath(sys.argv[0]))))
        os.chdir("..")
        self.setFixedSize(600, 300)
        self.setStyleSheet("background-color: black;")

        self.chan1 = QString()
        self.chan2 = QString()
        self.chan3 = QString()
        self.chan4 = QString()
        self.chan5 = QString()
        self.chan6 = QString()
        self.temp1 = QString()

        self.styles = styles()

        self.slider1 = QtGui.QSlider(1, self)
        self.slider2 = QtGui.QSlider(1, self)
        self.slider3 = QtGui.QSlider(1, self)
        self.slider4 = QtGui.QSlider(1, self)
        self.slider5 = QtGui.QSlider(1, self)
        self.slider6 = QtGui.QSlider(1, self)

        self.sliderList = [self.slider1, self.slider2, self.slider3, self.slider4, self.slider5, self.slider6]

        for slider in len(self.sliderList):
            slider.setFixedSize(500, 60)
            slider.setStyleSheet(self.styles.stylesheet())
            slider.move(20, 180)

        self.button = QtGui.QPushButton("OK", self)
        self.button.setStyleSheet(self.buttonstyle())
        self.button.setFixedSize(100, 60)
        self.button.move(420, 80)
        self.button.clicked.connect(app.quit)

        self.label = QtGui.QLabel("", self)
        self.label.setStyleSheet("color: white;")
        self.label.setFixedSize(600, 50)
        self.label.move(30, 30)

        # self.label.setText(os.getcwd()) # For debugging // May not need

        self.show()
        self.raise_()

class usbThread(QThread):

    channel1 = pyqtSignal(str)
    channel2 = pyqtSignal(str)
    channel3 = pyqtSignal(str)
    channel4 = pyqtSignal(str)
    channel5 = pyqtSignal(str)
    channel6 = pyqtSignal(str)
    temp1 = pyqtSignal(str)

    def __init__(self, parent):
        QThread.__init__(self, parent=None)
        self.name = "NanoThread"

    def run(self):
        while int(self.board_connected) == 1:
            self.parseData()

    def parseData(self):
        print "parsing"
        ## needs more CODE~!!



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