from PyQt5.QtCore import QRect, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QGraphicsView

from UI_BingMap import Ui_MainWindow
from bing_map import BingMap
from TileSystem import PixelXYToLatLong


class MainWindowBingo(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindowBingo, self).__init__(parent)
        self.setupUi(self)
        self.scene = BingMap((48.8584, 2.2945), 16, QRect(self.View.geometry().x(), self.View.geometry().y(),
                                                          self.View.geometry().width(), self.View.geometry().height()))
        self.View.setScene(self.scene)
        self.lineEditLatitude.setText(str(self.scene.get_coordonnees()[0]))
        self.lineEditLongitude.setText(str(self.scene.get_coordonnees()[1]))
        self.spinBoxZoom.setValue(self.scene.get_zoom())
        self.View.centerOn(self.scene.get_pixel_center()[0], self.scene.get_pixel_center()[1])
        self.View.resizeEvent = self.on_View_resize
        self.View.wheelEvent = self.on_View_wheelEvent
        self.moveView = False
        self.View.mousePressEvent = self.on_View_mousePress
        self.View.mouseReleaseEvent = self.on_View_mouseRelease
        self.lineEditLatitude.textChanged.connect(self.on_lineEditLatitude_textChanged)
        self.show()

    def on_View_mousePress(self, event):
        self.moveView = True
        self.pos = self.View.mapToScene(event.pos())

    def on_View_mouseRelease(self, event):
        if self.moveView:
            newpos = self.View.mapToScene(event.pos())
            self.scene.move_center(newpos.x() - self.pos.x(), newpos.y() - self.pos.y())
            print(str(newpos.x() - self.pos.x()) + ',' + str(newpos.y() - self.pos.y()))
            self.moveView = False
            coo = self.scene.get_coordonnees()
            self.lineEditLatitude.setText(str(coo[0]))
            self.lineEditLongitude.setText(str(coo[1]))

    def on_View_resize(self, event):
        self.scene.update_surface(
            QRect(self.View.geometry().x(), self.View.geometry().y(), event.size().width(), event.size().height()))
        self.scene.update_view()
        self.View.centerOn(self.scene.get_pixel_center()[0], self.scene.get_pixel_center()[1])

    def on_View_wheelEvent(self, e):
        if e.angleDelta().y() < 0:
            self.spinBoxZoom.setValue(self.spinBoxZoom.value() - 1)
        else:
            self.spinBoxZoom.setValue(self.spinBoxZoom.value() + 1)

    @pyqtSlot(int)
    def on_spinBoxZoom_valueChanged(self, i):
        self.scene.set_zoom(i)
        self.scene.update_surface(
            QRect(self.View.geometry().x(), self.View.geometry().y(), self.View.geometry().width(),
                  self.View.geometry().height()))
        self.scene.update_view()
        self.View.centerOn(self.scene.get_pixel_center()[0], self.scene.get_pixel_center()[1])

    def on_lineEditLatitude_textChanged(self):
        if self.lineEditLatitude.text() and self.lineEditLongitude.text():
            self.scene.set_coordonnees((float(self.lineEditLatitude.text()), float(self.lineEditLongitude.text())))
        self.scene.update_surface(
            QRect(self.View.geometry().x(), self.View.geometry().y(), self.View.geometry().width(),
                  self.View.geometry().height()))
        self.scene.update_view()
        self.View.centerOn(self.scene.get_pixel_center()[0], self.scene.get_pixel_center()[1])
