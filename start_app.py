import sys
from PyQt5.QtWidgets import QApplication
from main_window_Bingo import MainWindowBingo

app = QApplication(sys.argv)
mainWindow = MainWindowBingo()
mainWindow.show()

sys.exit(app.exec_())
