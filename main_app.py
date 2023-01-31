import sys
from functools import partial
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QDialogButtonBox,
    QApplication,
    QMainWindow,
    QWidget,
    QDialog
)

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Music Transcriber")

        dlg = WelcomeDialog(self)
        if dlg.exec():
            print("Success!")

        self.grid_width = 10
        self.instruments = [['red', 'Drums'],
                       ['blue', 'Piano'],
                       ['green', 'Guitar'],
                       ['purple', 'Bass']]

        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()
        self.button_grid = QGridLayout()

        self.song_button = QPushButton("Song Info")
        self.song_button.setMaximumWidth(80)
        self.song_button.clicked.connect(self.song_button_clicked)
        layout2.addWidget(self.song_button)

        self.track = QLabel('Track')
        self.track.setStyleSheet('QLabel {font-size: 25px;}')
        self.track.setMaximumHeight(50)
        layout2.addStretch()
        layout2.addWidget(self.track)
        layout2.addStretch()

        layout1.addLayout(layout2)

        #add track titles

        self.button_grid.setSpacing(10)

        self.populate_grid()


        layout1.setStretch(0,2)
        layout1.setStretch(1,8)

        layout1.addLayout(self.button_grid)

        self.new_instrument = QLineEdit()
        self.new_instrument.setPlaceholderText("Add Instrument")

        self.instrument_text = ""
        self.new_instrument.textChanged.connect(self.new_instrument_edited)
        self.new_instrument.returnPressed.connect(self.new_instrument_return_pressed)

        layout4 = QHBoxLayout()
        layout4.addWidget(self.new_instrument)
        tutorial_button = QPushButton("Tutorial")
        tutorial_button.clicked.connect(self.tutorial_clicked)
        layout4.addWidget(tutorial_button)

        layout1.addLayout(layout4)

        layout1.setContentsMargins(20,20,20,20)
        layout1.setSpacing(10)


        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)

    def populate_grid(self):
        for i in range(len(self.instruments)):
            if i == 0:
                self.button_grid.addWidget(QLabel("Instruments"),0,0)
            self.button_grid.addWidget(QLineEdit(text=self.instruments[i][1]), i+1, 0)
            self.button_grid.itemAtPosition(i+1, 0).widget().setStyleSheet(
                'QWidget{ background-color: ' + self.instruments[i][0] + ';}')
            self.button_grid.itemAtPosition(i,0).widget().setMinimumWidth(100)
            for j in range(self.grid_width):
                if i == 0:
                    self.button_grid.addWidget(QLineEdit(text="Section " + str(j+1)),i,j+1)
                    self.button_grid.itemAtPosition(i,j+1).widget().setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                # a = AdvancedButton("Test Button " + str(i) + "," + str(j), i, j+1)
                a = AdvancedButton("", i+1, j + 1)
                a.clicked.connect(partial(self.button_click_function, a.row, a.column, self.instruments[i][0]))
                # print(a)
                a.setCheckable(True)
                a.setMinimumHeight(80)
                a.setMinimumWidth(150)
                # print(a.isChecked())
                self.button_grid.addWidget(a, i+1, j + 1)

    def button_click_function(self, row, column, color):
        #print("Button Value : " + str(row) + ", " + str(column))
        button = self.button_grid.itemAtPosition(row,column).widget()
        if button.isChecked():
            button.setStyleSheet('QPushButton{ background-color: '+ color +';}')
        else:
            button.setStyleSheet('')

    def new_instrument_edited(self, s):
        self.instrument_text = s

    def new_instrument_return_pressed(self):
        dlg = ConfirmDialog(self)
        if dlg.exec():
            self.instruments.append(["orange",self.instrument_text])
            self.instrument_text = ""
            self.new_instrument.setText("")
            self.populate_grid()

    def tutorial_clicked(self):
        self.tutorial_window = Tutorial_Window()
        self.tutorial_window.show()

    def song_button_clicked(self, s):
        self.song_window = Song_Window()
        self.song_window.enterClicked.connect(self.on_song_entered)
        self.song_window.show()

    def on_song_entered(self,s):
        self.track.setText(s)

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

class AdvancedButton(QPushButton):
    def __init__(self, button_name, row, column):
        QPushButton.__init__(self, button_name)
        self.name = button_name
        self.row = row
        self.column = column

class Song_Window(QDialog):
    enterClicked = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.song_title = ""
        self.setWindowTitle("Song Settings")

        self.song_entry = QLineEdit()

        self.enter_button = QPushButton()
        self.enter_button.setText("Enter")

        self.layout = QVBoxLayout()
        message = QLabel("Enter Song Title")

        self.enter_button.clicked.connect(self.enter_clicked)

        self.layout.addWidget(message)
        self.layout.addWidget(self.song_entry)
        self.layout.addWidget(self.enter_button)
        self.setLayout(self.layout)

    def enter_clicked(self):
        if self.song_entry != "":
            self.enterClicked.emit(self.song_entry.text())
        self.close()

class Tutorial_Window(QDialog):
    enterClicked = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.tutorial_text = '''
        Song Info - On the top left of the main window, the "Song Info" button will take you to the Song Info window.
        There, the song title can be entered, which will then be displayed at the top of the main window.
        
        Song Grid - The grid layout represents a timeline of the song being transcribed. Each column represents a
        section of the song, while each row represents the instruments in the song.
        
        Sections - The top row of the grid shows the sections of the song, which can be renamed for each section of the
        song being transcribed.
        
        Instruments - The left-most column is a list of instruments in the song. It starts with some example instruments
        but they can be renamed.
        
        Add Instrument Button - Below the song grid is a text box that can be used to add a new instrument name. When 
        entering a name, you will be prompted to confirm this as it cannot be undone.
        
        Grid Boxes - Each box can be clicked to be colored in, representing that the instrument in this row is active
        during the section of the song this column represents
        
        When complete, the grid can be used as a visual reference for analyzing this song's structure.
        Taking a screenshot will allow this to be saved and referenced later.
        
        Taking a Screenshot:
        Mac: Command + Shift + 4
        Windows: Windows Key + Shift + S
        '''

        self.setWindowTitle("Tutorial")

        self.tutorial = QLabel(self.tutorial_text)

        self.enter_button = QPushButton()
        self.enter_button.setText("Okay")

        self.layout = QVBoxLayout()
        title = QLabel("Tutorial")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.enter_button.clicked.connect(self.okay_clicked)

        self.layout.addWidget(title)
        self.layout.addWidget(self.tutorial)
        self.layout.addWidget(self.enter_button)
        self.setLayout(self.layout)
    def okay_clicked(self,s):
        self.close()

class WelcomeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Welcome!")
        QBtn = QDialogButtonBox.StandardButton.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        message = QLabel('''
        Welcome! This application is designed to be a tool for analyzing song structure.
        
        While listening to a song, for each section of the song (chorus, verse, etc.), 
        enable which instruments are active during that section for a visual representation
        of the songs structure.
        
        For a detailed tutorial with all of the functions, click the "Tutorial" button on 
        the bottom right of the main window.
        ''')
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class ConfirmDialog(QDialog):
    confirmed = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Instrument Confirmation")

        QBtn = QDialogButtonBox.StandardButton.Ok |  QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Are you sure you want to add another instrument? \n (Cannot Be Undone)")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

app = QApplication(sys.argv)
app.setStyleSheet('QWidget {background-color: "gray";}')
main_win = MainWindow()
available_size = main_win.screen().availableGeometry()
#main_win.resize(int(available_size.width()*.2), int(available_size.height()*.2))
main_win.show()

app.exec()
