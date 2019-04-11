import sys

from PyQt5 import QtCore, QtGui, QtWidgets, uic

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('test.ui', self)
	self.onButton.clicked.connect(self.turnOn)
	self.offButton.clicked.connect(self.turnOff)
	self.intensitySlider.valueChanged.connect(self.value)

    def turnOn(self):
	print("hello")

    def turnOff(self):
	print("off")

    def value(self):
	print(self.intensitySlider.value())

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
