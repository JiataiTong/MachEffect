import sys

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, \
    QHBoxLayout
from PyQt6.QtGui import QColor

standard_voltage_value = 15
epsilon = 1e-2

# Sample batteryData
batteryData = []
for arm_index in range(8):
    for battery_index in range(6):
        voltage_value = standard_voltage_value + (arm_index - 4) * epsilon  # This will create some yellow cells
        if arm_index == 0 and battery_index == 0:  # Make one cell red for testing
            voltage_value = -1
        batteryData.append([arm_index, battery_index, voltage_value])

class BatteryCheckPage(QWidget):
    def __init__(self, main_page):
        super().__init__()
        self.main_page = main_page
        self.setWindowTitle("Battery Check Page")

        layout = QVBoxLayout()

        # Split the batteryData into two
        half_length = len(batteryData) // 2
        batteryData1 = batteryData[:half_length]
        batteryData2 = batteryData[half_length:]

        # Horizontal layout for tables
        table_layout = QHBoxLayout()

        # Table 1
        self.table1 = self.create_table(batteryData1)
        table_layout.addWidget(self.table1)

        # Table 2
        self.table2 = self.create_table(batteryData2)
        table_layout.addWidget(self.table2)

        layout.addLayout(table_layout)

        # Return button
        btn_layout = QHBoxLayout()
        self.return_button = QPushButton("Return to Main Page", self)
        self.return_button.clicked.connect(self.return_to_main)
        btn_layout.addWidget(self.return_button)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # Adjust the table widths to fit content
        self.table1.resizeColumnsToContents()
        self.table2.resizeColumnsToContents()

        # Calculate total width required for both tables
        total_width = self.table1.verticalHeader().width() + sum(
            [self.table1.columnWidth(i) for i in range(self.table1.columnCount())])
        total_width += self.table2.verticalHeader().width() + sum(
            [self.table2.columnWidth(i) for i in range(self.table2.columnCount())])

        # Add some buffer for window borders and potential scrollbars
        total_width += 50

        # Resize the window to fit the tables
        self.resize(total_width, self.height())

    def create_table(self, data):
        table = QTableWidget(len(data), 3, self)

        # Hide the vertical headers (row indices)
        table.verticalHeader().hide()

        table.setHorizontalHeaderLabels(["arm_index", "battery_index", "voltage_value"])
        for i, row_data in enumerate(data):
            arm_index, battery_index, voltage_value = row_data
            table.setItem(i, 0, QTableWidgetItem(str(arm_index)))
            table.setItem(i, 1, QTableWidgetItem(str(battery_index)))
            voltage_item = QTableWidgetItem(str(voltage_value))

            # Coloring based on voltage_value
            if voltage_value < 0:
                voltage_item.setBackground(QColor('red'))
            elif abs(voltage_value - standard_voltage_value) > epsilon:
                voltage_item.setBackground(QColor('yellow'))

            table.setItem(i, 2, voltage_item)
        return table

    def return_to_main(self):
        self.main_page.show()
        self.close()




# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main_page = QWidget()
#     ex = BatteryCheckPage(main_page)
#     ex.show()
#     sys.exit(app.exec())
