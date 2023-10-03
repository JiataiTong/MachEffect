from PyQt6.QtWidgets import (QMessageBox, QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QTableWidget, QGraphicsView, QTableWidgetItem)
import sys
import serial
import time
from PyQt6.QtCore import QTimer
from pyqtgraph import GraphicsLayoutWidget
import pandas as pd
from VoltageReader import VoltageReader


color_dict = { 0:"k", 1:'b', 2:'g', 3:'r', 4:'c', 5: 'm', 6:'y'}

def show_popup(message):
    msg = QMessageBox()
    msg.setWindowTitle("Alert")
    msg.setText(message)
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()


class ExperimentPage(QWidget):
    def __init__(self, main_page):
        super().__init__()
        self.main_page = main_page
        self.initUI()

        self.data_df = pd.DataFrame()
        self.reader_list = []
        for i in range(8):
            reader = VoltageReader(i)
            if reader.board is None:
                show_popup(f'Cannot read from board ${i}!')
            self.reader_list.append(reader)

        self.start_ts = -1

        # Call the start_experiment method
        self.start_experiment()

        # Set up the timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.read_and_update_data)
        self.timer.start(1000)  # 1 second interval

        # Set up a counter for the number of readings
        self.reading_count = 0

    def initUI(self):
        layout = QVBoxLayout()

        # 1. Create the main layout for the ExperimentPage.
        self.stacked_widget = QStackedWidget(self)

        # 2. Add a button to switch between the real-time plot widget and the table widget.
        self.switch_button = QPushButton("Switch to Table", self)
        self.switch_button.clicked.connect(self.toggle_view)
        layout.addWidget(self.switch_button)

        # 3. Add placeholders for the real-time plot and the table.
        self.plot_layout_widget = GraphicsLayoutWidget(self)  # Create a GraphicsLayoutWidget for plots
        self.plots = [] # To locate the right plot in an easier way.
        for i in range(4):  # 4 rows
            for j in range(2):  # 2 columns
                plot = self.plot_layout_widget.addPlot(row=i, col=j)  # Add a plot to the grid
                self.plots.append(plot)
        self.stacked_widget.addWidget(self.plot_layout_widget)

        # Placeholder for table
        self.table_widget = QTableWidget(self)
        self.stacked_widget.addWidget(self.table_widget)

        layout.addWidget(self.stacked_widget)

        # 4. Add a label to display the elapsed time.
        self.time_label = QLabel("Time Elapsed: 0 seconds", self)
        layout.addWidget(self.time_label)

        # 5. Add the return button to go back to the main page.
        self.return_button = QPushButton("Return to Main Page", self)
        self.return_button.clicked.connect(self.return_to_main)
        layout.addWidget(self.return_button)

        self.setLayout(layout)
        self.setWindowTitle('Experiment Page')

    def start_experiment(self):
        try:
            # Open the serial connection to the selected COM port
            ser = serial.Serial(self.main_page.selectedCOM, 9600)
            time.sleep(2)  # Wait for the serial connection to initialize.
            self.start_ts = time.time()

            # Send the "START" message
            ser.write(b'START\n')

            # Close the serial connection
            ser.close()

            # Start the timer after sending the start signal
            self.timer.start()

        except Exception as e:
            # Handle any exceptions that might occur
            print(f"Error: {e}")

    def get_voltage_from_board(self):
        data_rows = []
        for i in range(8):
            data_row = [i]
            voltage_list = self.reader_list[i].get_voltage()
            current_ts = time.time() - self.start_ts
            data_row.append(current_ts)
            data_row.extend(voltage_list)
            data_rows.append(data_row)
        return data_rows

    def read_and_update_data(self):
        # Increment the reading count
        self.reading_count += 1

        # Read data from the board
        data_rows = self.get_voltage_from_board()

        for data_row in data_rows:
            # Append data to the dataframe
            self.data_df = self.data_df.append(data_row, ignore_index=True)

            # Update the plot and table with new data
            self.update_plot(data_row)
            self.update_table(data_row)

        # If 360 seconds have passed, stop the timer and save the data
        if self.reading_count >= 360:
            self.timer.stop()
            self.data_df.to_csv('filename.csv', index=False, header=False)

    def update_plot(self, data_row):
        arm_index = data_row[0]
        time_stamp = data_row[1]
        voltage_values = data_row[2:]

        # Locate the plot using arm_index
        plot = self.plots[arm_index]

        # Update the plot with new data
        for i, voltage in enumerate(voltage_values):
            # Check if a curve for this voltage already exists, if not create one
            if len(plot.listDataItems()) <= i:
                curve = plot.plot(pen=color_dict[i])
            else:
                curve = plot.listDataItems()[i]

            # Append new data to the curve
            curve.setData(x=[time_stamp], y=[voltage], clear=False, _callSync='off')


    def update_table(self, data_row):
        # Extract arm index, timestamp, and voltage values from the data row
        arm_idx, timestamp, *voltages = data_row

        # Calculate the starting row for the given arm index
        starting_row = arm_idx * 6  # 6 batteries per arm

        # Update voltage values for each battery on the given arm
        for battery_idx, voltage in enumerate(voltages):
            # Find the row corresponding to the current battery
            row_position = starting_row + battery_idx

            # Update the voltage value for the current battery
            self.table.setItem(row_position, 2, QTableWidgetItem(str(voltage)))

    def toggle_view(self):
        current_index = self.stacked_widget.currentIndex()
        if current_index == 0:
            self.stacked_widget.setCurrentIndex(1)
            self.switch_button.setText("Switch to Plot")
        else:
            self.stacked_widget.setCurrentIndex(0)
            self.switch_button.setText("Switch to Table")

    def return_to_main(self):
        self.main_page.show()
        self.close()

# For testing purposes
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_page = QWidget()  # Dummy main page for testing
    ex = ExperimentPage(main_page)
    ex.show()
    sys.exit(app.exec())
