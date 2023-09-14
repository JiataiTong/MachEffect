import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtWidgets import QComboBox
import serial.tools.list_ports
from BatteryCheckPage import *
from CheckDataPage import *


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Create and populate the COM port selection combo box
        self.combo_com_ports = QComboBox(self)

        available_ports = [port.device for port in serial.tools.list_ports.comports()]
        if not available_ports:
            available_ports = ["COM1", "COM2", "COM3", "COM4"]
        self.combo_com_ports.addItems(available_ports)
        layout.addWidget(self.combo_com_ports)

        # Create buttons
        self.btn_battery_check = QPushButton('Battery Check', self)
        self.btn_control_test = QPushButton('Control Test', self)
        self.btn_experimental_test = QPushButton('Experimental Test', self)
        self.btn_check_data = QPushButton('Check Data', self)

        # Connect buttons to their respective functions
        self.btn_battery_check.clicked.connect(self.battery_check)
        self.btn_control_test.clicked.connect(self.control_test)
        self.btn_experimental_test.clicked.connect(self.experimental_test)
        self.btn_check_data.clicked.connect(self.check_data)

        # Add buttons to the layout
        layout.addWidget(self.btn_battery_check)
        layout.addWidget(self.btn_control_test)
        layout.addWidget(self.btn_experimental_test)
        layout.addWidget(self.btn_check_data)

        self.setLayout(layout)
        self.setWindowTitle('My App')
        self.setGeometry(300, 300, 300, 200)

    def battery_check(self):
        self.window = BatteryCheckPage(self)
        self.window.show()
        self.hide()

    def control_test(self):
        self.window = ControlTestPage(self)
        self.window.show()
        self.hide()

    def experimental_test(self):
        self.window = ExperimentalTestPage(self)
        self.window.show()
        self.hide()

    def check_data(self):
        self.window = CheckDataPage(self)
        self.window.show()
        self.hide()

    def get_selected_com(self):
        return self.combo_com_ports.currentText()


class BaseSubPage(QWidget):
    def __init__(self, main_page):
        super().__init__()
        self.main_page = main_page
        layout = QVBoxLayout()
        self.return_button = QPushButton("Return to Main Page", self)
        self.return_button.clicked.connect(self.return_to_main)
        layout.addWidget(self.return_button)
        self.setLayout(layout)

    def return_to_main(self):
        self.main_page.show()
        self.close()


# class BatteryCheckPage(BaseSubPage):
#     def __init__(self, main_page):
#         super().__init__(main_page)
#         self.setWindowTitle("Battery Check Page")
#         label = QLabel("This is the Battery Check Page")
#         self.layout().insertWidget(0, label)


class ControlTestPage(BaseSubPage):
    def __init__(self, main_page):
        super().__init__(main_page)
        self.setWindowTitle("Control Test Page")
        label = QLabel("This is the Control Test Page")
        self.layout().insertWidget(0, label)


class ExperimentalTestPage(BaseSubPage):
    def __init__(self, main_page):
        super().__init__(main_page)
        self.setWindowTitle("Experimental Test Page")
        label = QLabel("This is the Experimental Test Page")
        self.layout().insertWidget(0, label)


# class CheckDataPage(BaseSubPage):
#     def __init__(self, main_page):
#         super().__init__(main_page)
#         self.setWindowTitle("Check Data Page")
#         label = QLabel("This is the Check Data Page")
#         self.layout().insertWidget(0, label)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
