import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsView
from PyQt5.QtCore import QRect, Qt
from bing_map import BingMap


class Test(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 1024, 768)
        self.setWindowTitle("test map")
        scene = BingMap((48.8584, 2.2945), 16, QRect(self.geometry().x(), self.geometry().y(), self.geometry().width(), self.geometry().height()))
        self.view = QGraphicsView(scene, self)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.centerOn(scene.get_pixel_center()[0],scene.get_pixel_center()[1])
        self.show()


def main():
    app = QApplication(sys.argv)
    ex = Test()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
