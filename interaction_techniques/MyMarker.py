# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore


class MyMarker(QtGui.QGraphicsRectItem):
    def __init__(self, rect, y_absolute):
        QtGui.QGraphicsRectItem.__init__(self, rect)
        self.qobject = QtCore.QObject()
        self.graphics_rect = rect
        self.y_absolute = y_absolute
        self.icon = QtGui.QPixmap("icon.png")
        self.positionY = y_absolute
        self.counter = 0

    def rect(self):
        return self.graphics_rect

    def getQObject(self):
        return self.qobject

    def paint(self, painter, option, widget):
        print "Paint marker"
        #qp = QtGui.QPen()
        #qp.setBrush(QtGui.QColor(255, 0, 0))
        #painter.setPen(qp)
        self.counter += 1
        print "Drawing rect X:", self.graphics_rect.x()
        print "Drawing rect Y:", self.graphics_rect.y()
        print "Drawing rect Width:", self.graphics_rect.width()
        print "Drawing rect Height:", self.graphics_rect.height()
        print self.positionY

        drawing_rect = QtCore.QRect(self.graphics_rect.x(), self.graphics_rect.y(),
            self.graphics_rect.width(), self.graphics_rect.height())
        """
        painter.fillRect(drawing_rect, QtGui.QColor(255, 0, 0))
        painter.drawRect(drawing_rect)
        """
        painter.drawPixmap(drawing_rect, self.icon)

    def hoverEnterEvent(self, event):
        QtGui.QGraphicsRectItem.hoverEnterEvent(self, event)
        self.qobject.emit(QtCore.SIGNAL("markerEntered"), self)

    def hoverLeaveEvent(self, event):
        QtGui.QGraphicsRectItem.hoverLeaveEvent(self, event)
        self.qobject.emit(QtCore.SIGNAL("markerLeft"))

    def saveScreenshot(self, pixmap, rect):
        self.pixmap = pixmap.copy(0, 0, rect.width() / 2, rect.height())

    def getScreenshot(self):
        return self.pixmap
