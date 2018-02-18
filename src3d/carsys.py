
from PyQt4 import QtCore, QtGui

from point3d import *
from matrix import *
import math


class CarSystem(QtGui.QGraphicsItem):
    Type = QtGui.QGraphicsItem.UserType + 2

    def __init__(self, range):
        QtGui.QGraphicsItem.__init__(self)
        q = 64
        self.range = range

        self.nodes = [None, None, [], [], []]

        self.angle = Point3d()
        self.projectType = 0
        self.nodes[0] = [Point3d(range, 0, 0), Point3d(0, range, 0), Point3d(0, 0, range)]
        self.nodes[1] = [Point3d(-range, 0, 0), Point3d(0, -range, 0), Point3d(0, 0, -range)]
        mul1 = [1, 1, -1, -1]
        mul2 = [1, -1, -1, 1]
        for j in xrange(4):
            self.nodes[2].append(Point3d(range - 4 * range / q, range / q * mul1[j], range / q * mul2[j]))
            self.nodes[3].append(Point3d(-range / q * mul1[j], -range + 4 * range / q, -range / q * mul2[j]))
            self.nodes[4].append(Point3d(range / q * mul1[j], range / q * mul2[j], range - 4 * range / q))

        self.savedNodes = [None, None, [], [], []]

        self.savedNodes[0] = [Point3d(range, 0, 0), Point3d(0, range, 0), Point3d(0, 0, range)]
        self.savedNodes[1] = [Point3d(-range, 0, 0), Point3d(0, -range, 0), Point3d(0, 0, -range)]
        for j in xrange(4):
            self.savedNodes[2].append(Point3d(range - 4 * range / q, range / q * mul1[j], range / q * mul2[j]))
            self.savedNodes[3].append(Point3d(-range / q * mul1[j], -range + 4 * range / q, -range / q * mul2[j]))
            self.savedNodes[4].append(Point3d(range / q * mul1[j], range / q * mul2[j], range - 4 * range / q))

        self.aff_matrix = Matrix(4, 4)
        self.aff_matrix.unitDiag()

        self.rxMat = Matrix(4, 4)
        self.rxMat.unitButLast()

        self.ryMat = Matrix(4, 4)
        self.ryMat.unitButLast()

        self.rzMat = Matrix(4, 4)
        self.rzMat.unitButLast()

        self.sMat = Matrix(4, 4)
        self.sMat.unitButLast()

        self.mMat = Matrix(4, 4)
        self.mMat.unitButLast()

        self.color = QtCore.Qt.black

    def toPath(self):
        man = self.projectType
        pathVisible = QtGui.QPainterPath()
        myPen = QtGui.QPen()
        myFont = QtGui.QFont()
        pathVisible.addText(QtCore.QPointF((self.nodes[0][0] + Point3d(-16, 16, 0)).toQPointF(man)), myFont, "X")
        pathVisible.addText(QtCore.QPointF((self.nodes[1][1] + Point3d(-16, 16, 0)).toQPointF(man)), myFont, "Y")
        pathVisible.addText(QtCore.QPointF((self.nodes[0][2] + Point3d(-16, 16, 0)).toQPointF(man)), myFont, "Z")

        for i in xrange(3):
            pathVisible.moveTo(self.nodes[0][i].toQPointF(man))
            pathVisible.lineTo(self.nodes[1][i].toQPointF(man))

        for i in xrange(3):
            for j in xrange(4):
                if (i != 1):
                    pathVisible.moveTo(self.nodes[0][i].toQPointF(man))
                else:
                    pathVisible.moveTo(self.nodes[1][i].toQPointF(man))
                pathVisible.lineTo(self.nodes[i + 2][j].toQPointF(man))
        return pathVisible

    # *******************************************************
    #  ---------  S C A L E   ---------
    # *******************************************************
    @QtCore.pyqtSignature("(double)")
    def setScaleX(self, whow):
        self.mMat[0][0] += whow

    @QtCore.pyqtSignature("(double)")
    def setScaleY(self, whow):
        self.mMat[1][1] += whow

    @QtCore.pyqtSignature("(double)")
    def setScaleZ(self, whow):
        self.mMat[2][2] += whow

    @QtCore.pyqtSignature("(double)")
    def setScaleAll(self, whow):
        self.mMat[3][3] += 1 / whow
        # *******************************************************

    #  ---------  S H I F T   ---------
    # *******************************************************
    @QtCore.pyqtSignature("(double)")
    def setShiftX(self, whow):
        self.sMat[0][3] += whow

    @QtCore.pyqtSignature("(double)")
    def setShiftY(self, whow):
        self.sMat[1][3] += whow

    @QtCore.pyqtSignature("(double)")
    def setShiftZ(self, whow):
        self.sMat[2][3] += whow

    # *******************************************************
    #  ---------  R O T A T E  ---------
    # *******************************************************
    @QtCore.pyqtSignature("(double)")
    def setRotX(self, angle):
        self.angle.x += angle
        angle = math.pi * angle / 180
        m = Matrix(4, 4)
        m[3][3] = m[0][0] = 1
        m[2][2] = m[1][1] = math.cos(angle)
        m[2][1] = math.sin(angle)
        m[1][2] = -m[2][1]
        self.rxMat = m * self.rxMat

    @QtCore.pyqtSignature("(double)")
    def setRotY(self, angle):
        self.angle.y += angle
        angle = math.pi * angle / 180
        m = Matrix(4, 4)
        m[3][3] = m[1][1] = 1
        m[2][2] = m[0][0] = math.cos(angle)
        m[0][2] = math.sin(angle)
        m[2][0] = -m[0][2]
        self.ryMat = m * self.ryMat

    @QtCore.pyqtSignature("(double)")
    def setRotZ(self, angle):
        self.angle.z += angle
        angle = math.pi * angle / 180
        m = Matrix(4, 4)
        m[3][3] = m[2][2] = 1
        m[0][0] = m[1][1] = math.cos(angle)
        m[1][0] = math.sin(angle)
        m[0][1] = -m[1][0]
        self.rzMat = m * self.rzMat

    def refreshAll(self):
        self.sMat.unit()
        self.mMat.unit()
        self.rxMat.unit()
        self.ryMat.unit()
        self.rzMat.unit()
        self.refresh()

    def refresh(self):
        pass;
        for i in xrange(len(self.savedNodes)):
            for j in xrange(len(self.savedNodes[i])):
                for k in xrange(3):
                    self.nodes[i][j][k] = self.savedNodes[i][j][k]

    def realloc(self):
        for nodes in self.nodes:
            for node in nodes:
                node.affTr(self.sMat)

    def resize(self):
        for nodes in self.nodes:
            for node in nodes:
                node.affTr(self.mMat)

    def rotate(self):
        self.aff_matrix = self.rxMat * self.ryMat * self.rzMat
        for nodes in self.nodes:
            for node in nodes:
                node.affTr(self.aff_matrix)

    def boundingRect(self):
        return self.toPath().boundingRect()

    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(self.boundingRect())
        return path

    def paint(self, painter, option, widget):
        pass;
        self.setZValue(10000)
        painter.setPen(QtGui.QPen(self.color, 1, QtCore.Qt.DashLine))
        painter.drawPath(self.toPath())
        #painter.drawPath(self.shape())
        #painter.drawRect(self.boundingRect())

