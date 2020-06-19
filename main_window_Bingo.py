from PyQt5.QtWidgets import QMainWindow, QVBoxLayout
from pyqtlet import L, MapWidget

from UI_BingMap import Ui_MainWindow


class MainWindowBingo(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindowBingo, self).__init__(parent)
        self.setupUi(self)

        self.mapWidget = MapWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.mapWidget)
        self.frameMap.setLayout(self.layout)

        self.map = L.map(self.mapWidget)
        self.map.setView([12.97, 77.59], 10)
        L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(self.map)
        self.marker = L.marker([12.934056, 77.610029])
        self.marker.bindPopup('Maps are a treasure.')
        self.map.addLayer(self.marker
                          )
        self.show()
