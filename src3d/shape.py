import math

from PyQt4 import QtCore, QtGui

from point3d import *
from matrix import *
from side import *


def mulPi(i):
    i = math.pi * i
    return i


class Shape(QtGui.QGraphicsItem):
    Type = QtGui.QGraphicsItem.UserType + 1

    def __init__(self):
        QtGui.QGraphicsItem.__init__(self)
        # IMPL
        self.sides = []
        self.nodes = []
        self.savedNodes = []
        self.shadowNodes = []
        self.angle = Point3d()
        self.shift = Point3d()

        # CRT
        self.paral = True
        self.invis = 0
        self.numGen = 0

        # FUNC
        self.funcAll = ""
        self.funcX = "0"
        self.funcY = "0"
        self.funcZ = "0"

        self.inX_t_h = 0
        self.inY_t_h = 0
        self.inZ_t_h = 0

        self.hTo = 0
        self.hFrom = 0
        self.tTo = 0
        self.tFrom = 0
        self.tStep = 1
        self.hStep = 1
        self.radius = 0

        # COLORS
        self.colorObj, self.colorRlight, self.colorLight = \
            QtGui.QColor(QtCore.Qt.green), \
            QtGui.QColor(QtCore.Qt.darkGreen), \
            QtGui.QColor(QtCore.Qt.white)

        # LIGHT
        self.inten = 0
        self.defRefl = 0
        self.mirRefl = 0
        self.mirPow = 0
        self.type = 0

        # SHW
        self.projectType = 0
        self.showNormals = False

        # SHADOW
        self.wall = 250
        self.alpha = 255
        self.alphaShadow = 255
        self.shadow = True

        # M A T R I X E S
        self.aff_matrix = Matrix(4, 4)
        self.rMat = Matrix(4, 4)
        self.rMat.unitButLast()
        self.sMat = Matrix(4, 4)
        self.sMat.unitButLast()
        self.mMat = Matrix(4, 4)
        self.mMat.unitButLast()
        self.rxMat = Matrix(4, 4)
        self.rxMat.unitButLast()
        self.ryMat = Matrix(4, 4)
        self.ryMat.unitButLast()
        self.rzMat = Matrix(4, 4)
        self.rzMat.unitButLast()

        # ACNION
        self.changeGen()
        self.lamp = Point3d()
        self.reBuild()

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
        self.shift.x = whow
        self.sMat[0][3] += whow

    @QtCore.pyqtSignature("(double)")
    def setShiftY(self, whow):
        self.shift.y = whow
        self.sMat[1][3] += whow

    @QtCore.pyqtSignature("(double)")
    def setShiftZ(self, whow):
        self.shift.z = whow
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

    @QtCore.pyqtSignature("(double)")
    def hToSlot(self, i):
        self.hTo = i * math.pi

    @QtCore.pyqtSignature("(double)")
    def hFromSlot(self, i):
        self.hFrom = i * math.pi

    @QtCore.pyqtSignature("(double)")
    def tToSlot(self, i):
        self.tTo = i * math.pi

    @QtCore.pyqtSignature("(double)")
    def tFromSlot(self, i):
        self.tFrom = i * math.pi

    @QtCore.pyqtSignature("(int)")
    def tStepSlot(self, i):
        self.tStep = math.pi / i

    @QtCore.pyqtSignature("(int)")
    def hStepSlot(self, i):
        self.hStep = math.pi / i

    def nodeGenerator(self):
        self.nodes = []
        self.savedNodes = []
        i = 0
        hStep = self.hStep
        tStep = self.tStep
        h = self.hFrom - 0.01
        while h <= self.hTo + 2 * tStep:
            self.nodes.append([])
            self.savedNodes.append([])
            t = self.tFrom
            while t <= self.tTo + 2 * tStep:
                try:
                    exec ("%s\nself.inX_t_h =  %s" % (self.funcAll, self.funcX));
                    exec ("%s\nself.inY_t_h =  %s" % (self.funcAll, self.funcY));
                    exec ("%s\nself.inZ_t_h = %s" % (self.funcAll, self.funcZ));
                except:
                    pass
                    return
                P = Point3d(self.inX_t_h, self.inY_t_h, self.inZ_t_h)
                P2 = Point3d(self.inX_t_h, self.inY_t_h, self.inZ_t_h)
                self.nodes[i].append(P)
                self.savedNodes[i].append(P2)
                t += tStep
            h += hStep
            i += 1

    def changeGen(self):
        if self.numGen == 0:
            self.numGen = 1
        if self.numGen == 1:
            self.numGen = 0

    def sideGenerator1(self):
        for side in self.sides:
            side.setParentItem(None)
        self.sides = []
        for i in xrange(len(self.nodes) - 3):
            for j in xrange(len(self.nodes[i]) - 3):
                side1 = Side(self)
                side1.nodes.append(self.nodes[i][j])
                side1.nodes.append(self.nodes[i][j + 1])
                side1.nodes.append(self.nodes[i + 1][j + 1])
                side1.nodes.append(self.nodes[i + 1][j])
                self.sides.append(side1)

    def sideGenerator2(self):
        for side in self.sides:
            side.setParentItem(None)
        self.sides = []
        side1 = Side(self)
        side2 = Side(self)
        for j in xrange(len(self.nodes[1]) - 1):
            side1.nodes.append(self.nodes[1][len(self.nodes[1]) - 2 - j])
        self.sides.append(side1)
        k = len(self.nodes) - 4
        for j in xrange(len(self.nodes[k]) - 1):
            side2.nodes.append(self.nodes[k][j])
        self.sides.append(side2)
        for i in xrange(len(self.nodes) - 4):
            for j in xrange(len(self.nodes[i]) - 3):
                if i == 0:
                    continue
                side1 = Side(self)
                side1.nodes.append(self.nodes[i][j])
                side1.nodes.append(self.nodes[i][j + 1])
                side1.nodes.append(self.nodes[i + 1][j + 1])
                side1.nodes.append(self.nodes[i + 1][j])
                self.sides.append(side1)

    def boo(self):
        for side in self.sides:
            side.setParentItem(None)
        self.sides = []
        for i in xrange(len(self.nodes) - 1):
            for j in xrange(len(self.nodes[i]) - 1):
                if i % 2 and j % 2:
                    side1 = Side(self)
                    side1.nodes.append(self.nodes[i][j])
                    side1.nodes.append(self.nodes[i][j + 1])
                    side1.nodes.append(self.nodes[i + 1][j + 1])
                    side1.nodes.append(self.nodes[i + 1][j])
                    self.sides.append(side1)

    def reBuild(self):
        self.nodeGenerator()
        if self.numGen == 0:
            self.sideGenerator1()
        if self.numGen == -1:
            self.boo()
        if self.numGen == 2:
            self.sideGenerator2()

    def refreshAll(self):
        self.sMat.unit()
        self.mMat.unit()
        self.rxMat.unit()
        self.ryMat.unit()
        self.rzMat.unit()
        self.refresh()

    def refresh(self):
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

    def globalCenter(self):
        sum = Point3d()
        for nodes in self.nodes:
            for node in nodes:
                sum += node
        return sum / (len(self.nodes) * len(self.nodes[1]))

    def boundingRect(self):
        penWidth = 1
        return QtCore.QRectF(-100 - penWidth / 2, -100 - penWidth / 2,
                             100 + penWidth / 2, 100 + penWidth / 2)

    def paint(self, painter, option, widget):
        path = QtGui.QPainterPath()

        for side in self.sides:

            side.cAmbient = self.colorObj
            side.cLamp = self.colorLight
            side.cDiffuse = self.colorRlight
            side.showNormals = self.showNormals

            side.kA = self.inten
            side.kD = self.defRefl
            side.kS = self.mirRefl
            side.kSpow = self.mirPow
            side.lamp = self.lamp
            side.alpha = self.alpha
            side.alphaShadow = self.alphaShadow
            side.visible = not self.invis
            side.paral = self.paral
            side.wall = self.wall
            side.projectType = self.projectType
            side.type = self.type

            try:
                side.paint(painter, option, widget)
                if self.shadow and self.wall != 0:
                    painter.setBrush(
                            QtGui.QBrush(QtGui.QColor(0, 0, 0, (self.alphaShadow * self.alpha / 255 * 100 / self.wall))))
                    painter.setPen(
                        QtGui.QPen(QtGui.QColor(0, 0, 0, (self.alphaShadow * self.alpha / 255 * 100 / self.wall) / 12)))
                    side.paint2(painter, option, widget)
            except:
                    print("There is err in Shape.paint()")

# --------------------------------------------------------------------------------
