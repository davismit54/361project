import sys
from PyQt6.QtCore import QTime
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTimeEdit,
    QVBoxLayout,
    QGridLayout,
    QWidget,
)

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("My App")

        self.bpm = 128
        self.minutes = 3.5
        self.bars = int(self.minutes * self.bpm / 4)
        self.title = ""


        song_box_layout = QVBoxLayout()
        bar_layout = QGridLayout()

        self.song_title = QLineEdit()
        self.bars_label = QLabel()
        bpm_line = QLineEdit()
        length = QTimeEdit()
        calculate_button = QPushButton(text="Calculate Beat Count")

        self.song_title.setPlaceholderText("Enter Song Title")
        self.song_title.textChanged.connect(self.song_title_changed)


        length.setMinimumTime(QTime(0,0,0))
        length.setMaximumTime(QTime(0,10,0))
        length.setDisplayFormat("mm:ss")

        bpm_line.setMaxLength(3)
        bpm_line.setPlaceholderText("Enter BPM")


        bpm_line.textChanged.connect(self.bpm_text_changed)
        calculate_button.clicked.connect(self.calculate)

        length.timeChanged.connect(self.time_changed)


        bar_layout.addWidget(QLabel(text="Length:"), 0, 0)
        bar_layout.addWidget(length,0,1)
        bar_layout.addWidget(QLabel(text="Beats Per Minute"), 1,0)
        bar_layout.addWidget(bpm_line,1,1)
        bar_layout.addWidget(QLabel(text="Bars:"), 2, 0)
        bar_layout.addWidget(self.bars_label, 2, 1)

        song_box_layout.addWidget(self.song_title)
        song_box_layout.addLayout(bar_layout)
        song_box_layout.addWidget(calculate_button)


        song_box = QWidget()
        song_box.setLayout(song_box_layout)

        self.setCentralWidget(song_box)


    def song_title_changed(self, s):
        print("title changed")
        self.title = s

    def title_return_pressed(self):
        self.song_title.setText(self.title)

    def calculate(self):
        print("calculate!")
        self.bars = int(self.minutes * self.bpm / 4)
        self.bars_label.setText(str(self.bars))
        print(self.minutes)
        print(self.bpm)

    def bpm_return_pressed(self):
        print("Return pressed!")
        print(self.minutes)
        self.bars_label.setText(str(int(self.bpm * self.minutes)))

    def bpm_text_changed(self, s):
        print("Text changed...")
        if s != "":
            self.bpm = int(s)

    def time_changed(self, t):
        print('time changed:')
        self.minutes = t.minute()+(t.second()/60)
        print(self.minutes)


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()