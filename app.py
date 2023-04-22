import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QFileDialog
from conv import *
from PyQt5.QtWidgets import QMessageBox, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('ATCC (ASS to CSV Converter)')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        label = QLabel('Click the button to process .ass files in a folder:')
        layout.addWidget(label)

        btn_process_files = QPushButton('Process .ass files', self)
        btn_process_files.clicked.connect(self.process_files)
        layout.addWidget(btn_process_files)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def process_files(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select folder containing .ass files')
        if folder_path:
            csv_file_path, _ = QFileDialog.getSaveFileName(self, 'Save CSV file', filter='CSV files (*.csv)')
            if csv_file_path:
                if not csv_file_path.lower().endswith('.csv'):
                    csv_file_path += '.csv'

                process_all_ass_files(folder_path, csv_file_path)
                QMessageBox.information(self, 'Success', 'The .ass files have been processed and saved to the .csv file.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())