#!/usr/bin/python
import serial, os, sys
from PyQt4 import QtGui
from PyQt4.QtCore import QString, QThread

class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        os.chdir(str(os.path.dirname(os.path.abspath(sys.argv[0]))))
        os.chdir("..")
        self.setFixedSize(600, 300)
        self.setStyleSheet("background-color: black;")

        self.styles = styles()
        self.warp1_slider = QtGui.QSlider(1, self)
        self.warp1_slider.setFixedSize(500, 60)
        self.warp1_slider.sliderMoved.connect(self.calc_slider1)
        self.warp1_slider.setStyleSheet(self.stylesheet())
        self.warp1_slider.setMaximum(-4000)
        self.warp1_slider.setMinimum(-8000)
        self.warp1_slider.setValue(-5000)
        self.warp1_slider.move(20, 180)

        self.button = QtGui.QPushButton("OK", self)
        self.button.setStyleSheet(self.buttonstyle())
        self.button.setFixedSize(100, 60)
        self.button.move(420, 80)
        self.button.clicked.connect(app.quit)

        self.arrow = QtGui.QPushButton(self)
        self.arrow.setStyleSheet(self.arrowstyle())
        self.arrow.setFixedSize(55, 100)
        self.arrow.move(50, 30)

        self.label = QtGui.QLabel("", self)
        self.label.setStyleSheet("color: white;")
        self.label.setFixedSize(600, 50)
        self.label.move(30, 30)

        self.label.setText(os.getcwd())

        self.show()
        self.raise_()



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

    def arrowstyle(self):

        return """
            QPushButton {
                background-image: url(Resources/arrowLeft_normal.jpg);
                border-style: inset;
            }
            QPushButton::pressed {
                border-style: inset;
                image: url(Resources/arrowLeft_pressed.jpg);
            }
        """

app = QtGui.QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())