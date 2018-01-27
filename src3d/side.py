import math

from PyQt4 import QtCore, QtGui

from point3d import *
from matrix import *


class Side(QtGui.QGraphicsItem):
    Z = Point3d(0, 0, 1)

    def __init__(self, parent):
        QtGui.QGraphicsItem.__init__(self, parent)
        # IMPLEMENTATION
        self.visible = 0
        self.nodes = []
        self.shadNodes = []
        # Proj:
        self.projectType = 0
        self.lamp = Point3d(0, 0, -1000)
        # VEC:
        self.globalCenter = None
        self.centerPoint = None
        self.normalVector = None
        # SHADOWING:
        self.shadZ = -250
        self.wall = 250
        self.alpha = 255
        self.alphaShadow = 255
        self.paral = 2
        self.shadowMatrix = Matrix(4, 4)
        self.shadowMatrix.unitDiag()

        self.fading = 0
        # COLOR
        self.kA = 0
        self.kD = 0
        self.kS = 0
        self.kSpow = 0
        self.type = 0
        # COLOR REAL !
        self.cAmbient = QtGui.QColor()
        self.cLamp = QtGui.QColor()
        self.cDiffuse = QtGui.QColor()
        self.showNormals = False

    def genShadowMat(self):
        self.shadNodes = []
        if (self.lamp.z <= 0):
            return

        self.shadowMatrix[0][2] = -(self.lamp.x) / (self.lamp.z)
        self.shadowMatrix[1][2] = -(self.lamp.y) / (self.lamp.z)
        self.shadowMatrix[2][0] = -(250)
        self.shadowMatrix[2][1] = -(250)

        if (self.paral == 2):
            for node in self.nodes:
                nd = Point3d()
                nd.x = node.x - (self.wall - node.z) * self.lamp.x / self.lamp.z
                nd.y = node.y + (self.wall - node.z) * self.lamp.y / self.lamp.z
                self.shadNodes.append(nd)
        else:
            for node in self.nodes:
                nd = Point3d()
                nd.x = (- node.x * self.lamp.z + (self.wall - node.z) * self.lamp.x) / (
                            node.z + self.wall - self.lamp.z)
                nd.y = (- node.y * self.lamp.z + (self.wall - node.z) * self.lamp.y) / (
                            node.z + self.wall - self.lamp.z)
                nd.z = 0
                self.shadNodes.append(nd)

    def center(self):
        self.centerPoint = Point3d()
        self.centerPoint = sum3d(self.nodes) / len(self.nodes)
        return self.centerPoint

    def normal(self):
        p0 = self.nodes[2]
        p1 = self.nodes[1]
        p2 = self.nodes[0]
        self.normalVector = ((p1 - p0) ^ (p2 - p0))

        if (self.normalVector == Point3d(0, 0, 0)):
            p0 = self.nodes[2]
            p1 = self.nodes[1]
            p2 = self.nodes[3]
            self.normalVector = ((p1 - p0) ^ (p2 - p0))

        if (self.normalVector == Point3d(0, 0, 0)):
            p0 = self.nodes[2]
            p1 = self.nodes[0]
            p2 = self.nodes[3]
            self.normalVector = ((p1 - p0) ^ (p2 - p0))

        self.normalVector = norm(self.normalVector)
        return self.normalVector

    def light(self):
        self.fading = 0
        cA = ColorToPoint(self.cAmbient)
        cL = ColorToPoint(self.cLamp)
        cD = ColorToPoint(self.cDiffuse)
        vectorToLamp = self.lamp
        if (self.paral == 0):
            vectorToLamp = self.lamp - self.centerPoint
        d = abs(vectorToLamp) / 200
        L = norm(vectorToLamp)
        N = self.normal()
        S = norm(Point3d(0, 0, -1000) - self.centerPoint)
        R = Point3d()
        
        R.x = N.z * (N.x * L.z - N.z * L.x) - N.y * (N.y * L.x - N.x * L.y) + N.x * (N.x * L.x + N.y * L.y + N.z * L.z)
        R.y = -N.z * (N.z * L.y - N.y * L.z) + N.x * (N.y * L.x - N.x * L.y) + N.y * (N.x * L.x + N.y * L.y + N.z * L.z)
        R.z = N.y * (N.z * L.y - N.y * L.z) - N.x * (N.x * L.z - N.z * L.x) + N.z * (N.x * L.x + N.y * L.y + N.z * L.z)
        R = norm(R)

        try:
            H = (L + S) / abs(L + S)  # Light vector
        except:
            H = Point3d()

        LN = L | N
        if (self.type == 0):
            RS = H | N
        else:
            RS = R | S

        n = self.kSpow
        if (RS < 0):
            RS = 0
        else:
            RS = RS ** n
        rS = 0
        ln = 0

        self.cRes = QtGui.QColor(0, 0, 0, self.alpha)

        if (S | N <= 0):
            if (LN >= 0):
                ln = LN
            if (RS >= 0):
                rS = RS
        else:
            if (LN <= 0):
                ln = -LN
            if (RS <= 0):
                rS = -RS

        if (self.normalVector == Point3d(0, 0, 0)):
            self.cRes = QtGui.QColor(0, 0, 0, 255)
            return

        kA = self.kA
        kD = self.kD
        kS = self.kS

        d_mult = 1
        K = self.fading

        result = Point3d()
        for i in [0, 1, 2]:
            result[i] = kA * cA[i] * cD[i] + cL[i] * (kD * cD[i] * (ln) + kS * rS) / (d * d_mult + K)

        result = norm(result)
        self.cRes.setRedF(result[0])
        self.cRes.setGreenF(result[1])
        self.cRes.setBlueF(result[2])

    def __del__(self):
        pass;

    def setLamp(self, l):
        self.lamp = l

    def toQPolygonF(self, man=0):
        points = []
        for node in self.nodes:
            points.append(node.toQPointF(man))
        return QtGui.QPolygonF(points)

    def toShadowQPolygonF(self, man=0):
        points = []
        for node in self.shadNodes:
            points.append(node.toQPointF(man))
        return QtGui.QPolygonF(points)

    def zValue(self):
        zX = []
        for node in self.nodes:
            zX.append(node.z)
        zNum = sum(zX) / len(self.nodes)
        self.setZValue(zNum)
        return zNum

    def boundingRect(self):
        penWidth = 1
        return QtCore.QRectF(-100 - penWidth / 2, -100 - penWidth / 2,
                             100 + penWidth / 2, 100 + penWidth / 2)

    def paint2(self, painter, option, widget):
        self.setZValue(- 1000000)
        self.genShadowMat()

        painter.drawPolygon(self.toShadowQPolygonF(self.projectType))

    def paint(self, painter, option, widget):
        self.center()
        self.light()
        self.zValue()
        if self.visible:
            painter.setBrush(QtGui.QBrush(self.cRes))
        painter.setPen(QtGui.QPen(QtGui.QBrush(self.cRes), 2, QtCore.Qt.SolidLine))
        painter.drawPolygon(self.toQPolygonF(self.projectType))
        self.setToolTip("%s" % (self.center()))
        if self.showNormals:
            painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 255), 1, QtCore.Qt.DashDotDotLine))
            painter.drawLine((self.center() - self.normalVector).toQPointF(),
                             ((self.center() - self.normalVector) * 3).toQPointF())
