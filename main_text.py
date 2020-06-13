import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import QRect
from bing_map import BingMap


class Test(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 1024, 1024)
        self.setWindowTitle("test map")
        self.scene = BingMap((48.8584, 2.2945), 10, QRect(0, 0, 1024, 1024))
        self.view = QGraphicsView(self.scene, self)
        self.view.centerOn(self.scene.get_pixel_center()[0],self.scene.get_pixel_center()[1])
        self.show()


def main():
    app = QApplication(sys.argv)
    ex = Test()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
