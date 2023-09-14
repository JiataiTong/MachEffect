import sys
import os
import pandas as pd
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QCoreApplication
from pyqtgraph.exporters import ImageExporter


class CheckDataPage(QWidget):
    def __init__(self, main_page):
        super().__init__()
        self.main_page = main_page
        self.setWindowTitle("Check Data Page")

        layout = QVBoxLayout()

        # Drop-down selector
        self.comboBox = QComboBox(self)
        self.populate_combobox()
        self.comboBox.currentIndexChanged.connect(self.load_data)
        layout.addWidget(self.comboBox)

        # Plot
        self.plot_widget = pg.PlotWidget(self)
        layout.addWidget(self.plot_widget)

        # Create and add the save button to the QVBoxLayout
        self.save_button = QPushButton("Save Graph", self)
        self.save_button.clicked.connect(self.save_graph)
        layout.addWidget(self.save_button)

        # Return button
        self.return_button = QPushButton("Return to Main Page", self)
        self.return_button.clicked.connect(self.return_to_main)
        layout.addWidget(self.return_button)

        self.setLayout(layout)

    def populate_combobox(self):
        # Placeholder
        self.comboBox.addItem("Select a data file")

        # List all files in ./data directory
        data_directory = './data'
        data_files = [f for f in os.listdir(data_directory) if os.path.isfile(os.path.join(data_directory, f))]
        for file in data_files:
            self.comboBox.addItem(file)

    # def load_data(self):
    #     selected_file = self.comboBox.currentText()
    #     if selected_file == "Select a data file":
    #         self.plot_widget.clear()
    #         return
    #
    #     # Read the CSV file using pandas
    #     data_directory = './data'
    #     df = pd.read_csv(os.path.join(data_directory, selected_file), header=None, index_col=None)
    #
    #     # Reset the index of the DataFrame
    #     df.reset_index(drop=True, inplace=True)
    #
    #     # Clear previous plots
    #     self.plot_widget.clear()
    #
    #     # Create a GraphicsLayout
    #     layout = pg.GraphicsLayout()
    #     self.plot_widget.setCentralItem(layout)
    #     # print(df[0])
    #
    #     # Plot data
    #     for arm_index in df[0].unique():
    #         arm_data = df[df[0] == arm_index].reset_index(drop=True)
    #         # print(arm_data)
    #         plot_item = layout.addPlot(title=f"Arm {int(arm_index)}")
    #         for battery_index in range(2, 8):  # Columns 2 to 7 are battery data (0-based index)
    #             # Notations:
    #             # 0: arm index
    #             # 1: timestamp
    #             # 2-7: voltage values of the 6 batteries on each arm
    #             plot_item.plot(arm_data[1], arm_data[battery_index],
    #                            pen=pg.mkPen(color=pg.intColor(battery_index - 2, 6)))
    #         layout.nextRow()  # Move to the next row for the next plot

    def load_data(self):
        selected_file = self.comboBox.currentText()
        if selected_file == "Select a data file":
            self.plot_widget.clear()
            return

        # Read the CSV file using pandas
        data_directory = './data'
        df = pd.read_csv(os.path.join(data_directory, selected_file), header=None, index_col=None)

        # Sort the DataFrame by the timestamp column
        df = df.sort_values(by=[1])

        # Clear previous plots
        self.plot_widget.clear()

        # Create a GraphicsLayout with 2 columns
        layout = pg.GraphicsLayout(border=(100, 100, 100))
        self.plot_widget.setCentralItem(layout)

        # Plot data

        # for idx, arm_index in enumerate(df[0].unique()):
        #     arm_data = df[df[0] == arm_index].reset_index(drop=True)
        #
        #     # Determine which column to add the plot based on arm index
        #     col = 0 if idx < 4 else 1
        #     plot_item = layout.addPlot(row=idx % 4, col=col, title=f"Arm {int(arm_index)}")
        #
        #     for battery_index in range(2, 8):  # Columns 2 to 7 are battery data (0-based index)
        #         plot_item.plot(arm_data[1], arm_data[battery_index],
        #                        pen=pg.mkPen(color=pg.intColor(battery_index - 2, 6)))

        # Loop through each arm from 0 to 7
        for arm_index in range(len(df[0].unique())):
            arm_data = df[df[0] == arm_index].reset_index(drop=True)

            # Determine which column to add the plot based on arm index
            col = 0 if arm_index < 4 else 1
            plot_item = layout.addPlot(row=arm_index % 4, col=col, title=f"Arm {int(arm_index)}")

            for battery_index in range(2, 8):  # Columns 2 to 7 are battery data (0-based index)
                plot_item.plot(arm_data[1], arm_data[battery_index],
                               pen=pg.mkPen(color=pg.intColor(battery_index - 2, 6)))

    def save_graph(self):
        # Check if the default graph is displayed
        selected_file = self.comboBox.currentText()
        if selected_file == "Select a data file":
            return

        # Check if the ./graph directory exists, if not, create it
        graph_directory = './graph'
        if not os.path.exists(graph_directory):
            os.makedirs(graph_directory)

        # Save the graph with the same filename as the data (but with a .png extension)
        selected_file = self.comboBox.currentText()
        filename_without_extension = os.path.splitext(selected_file)[0]
        save_path = os.path.join(graph_directory, filename_without_extension + '.png')

        exporter = ImageExporter(self.plot_widget.scene())
        exporter.export(save_path)

        # Process all pending events to ensure the file is saved immediately
        QCoreApplication.processEvents()

    def return_to_main(self):
        self.main_page.show()
        self.close()


# Sample usage
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main_page = QWidget()
#     window = CheckDataPage(main_page)
#     window.show()
#     sys.exit(app.exec())
