from PyQt4 import QtCore, QtGui

from carsys import *
from shape import *
from plane import *
import sys
import os


def inside(R, P, offset=QtCore.QPoint(0, 0)):
    in_X = (R.left() + offset.x() <= P.x()) and (P.x() <= R.right() + offset.x())
    in_Y = (R.top() + offset.y() <= P.y()) and (P.y() <= R.bottom() + offset.y())
    return in_X and in_Y


class Graphic(QtGui.QGraphicsView):
    def __init__(self):
        QtGui.QGraphicsView.__init__(self)
        self.timerId = 0
        scene = QtGui.QGraphicsScene(self)
        scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        scene.setSceneRect(-self.size().width() / 2, -self.size().height() / 2, self.size().width(),
                           self.size().height())
        self.setScene(scene)
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        self.setViewportUpdateMode(QtGui.QGraphicsView.FullViewportUpdate)

        self.carSys = CarSystem(250)
        self.shape = Shape()

        scene.addItem(self.carSys)
        scene.addItem(self.shape)

        self.menuOut = QtGui.QMenu()

        self.menuOut.addSeparator()
        self.actBC = self.menuOut.addAction(self.trUtf8("перший колір фону"))
        self.backcolor = QtCore.Qt.white
        self.backGroundSetGrad(QtCore.Qt.black)
        self.connect(self.actBC, QtCore.SIGNAL("triggered( )"), self.backGroundChangeColor)

        self.actBG = self.menuOut.addAction(self.trUtf8("другий колір фону"))
        self.connect(self.actBG, QtCore.SIGNAL("triggered( )"), self.backGroundChangeGrad)

        self.picBG = self.menuOut.addAction(self.trUtf8("зображення для фону"))
        self.connect(self.picBG, QtCore.SIGNAL("triggered( )"), self.backGroundChangePic)

        self.menuOut.addSeparator()
        self.changeOut = [None, None, None]
        self.changeOut[0] = self.menuOut.addAction(self.trUtf8("змінювати вісь X"))
        self.changeOut[0].setCheckable(True)
        self.changeOut[0].setChecked(True)

        self.changeOut[1] = self.menuOut.addAction(self.trUtf8("змінювати вісь Y"))
        self.changeOut[1].setCheckable(True)
        self.changeOut[1].setChecked(True)

        self.changeOut[2] = self.menuOut.addAction(self.trUtf8("змінювати вісь Z"))
        self.changeOut[2].setCheckable(True)
        self.changeOut[2].setChecked(True)

        self.menuIn = QtGui.QMenu()
        self.rotate = self.menuIn.addAction(self.trUtf8("повернути"))
        self.rotate.setCheckable(True)
        self.rotate.setChecked(False)
        self.connect(self.rotate, QtCore.SIGNAL("triggered( bool )"), self.blockResizeCoord)

        self.menuIn.addSeparator()
        self.invisible = self.menuIn.addAction(self.trUtf8("тільки каркас"))
        self.invisible.setCheckable(True)
        self.invisible.setChecked(False)
        self.connect(self.invisible, QtCore.SIGNAL("triggered( bool )"), self.invisibility)

        self.paintShadow = self.menuIn.addAction(self.trUtf8("тінь"))
        self.paintShadow.setCheckable(True)
        self.paintShadow.setChecked(True)
        self.connect(self.paintShadow, QtCore.SIGNAL("triggered( bool )"), self.shadow)

        self.perspectiva = self.menuIn.addAction(self.trUtf8("перспектива"))
        self.perspectiva.setCheckable(True)
        self.perspectiva.setChecked(False)
        self.connect(self.perspectiva, QtCore.SIGNAL("triggered( bool )"), self.itemsPro)

        self.menuIn.addSeparator()
        self.ac = self.menuIn.addAction(self.trUtf8("колір осей"))
        self.connect(self.ac, QtCore.SIGNAL("triggered( )"), self.carSysChangeColor)

        self.menuIn.addSeparator()
        self.change = [None, None, None]
        self.change[0] = self.menuIn.addAction(self.trUtf8("змінити довжину"))
        self.change[0].setCheckable(True)
        self.change[0].setChecked(True)

        self.change[1] = self.menuIn.addAction(self.trUtf8("змінити висоту"))
        self.change[1].setCheckable(True)
        self.change[1].setChecked(True)

        self.change[2] = self.menuIn.addAction(self.trUtf8("змінити ширину"))
        self.change[2].setCheckable(True)
        self.change[2].setChecked(True)

        self.scale(1, 1)
        self.setMinimumSize(400, 400)

        # wheel
        self.wheelPos = 0
        self.mousePressed = False

        # mouse
        self.mousePressPos = QtCore.QPoint(0, 0)
        self.mousePressed = False
        self.carSys.angle.x = 1
        self.carSys.angle.y = 1
        self.shiftScale = 1
        # self.itemMoved()
        # self.printView()

    def printView(self):
        global painter
        i = False
        try:
            printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
            printer.setPageSize(QtGui.QPrinter.A4)
            painter = QtGui.QPainter(printer)
            i = True
        except:
            i = False
        self.render(painter)
        del painter

    @QtCore.pyqtSignature("bool")
    def shadow(self, p):
        self.shape.shadow = p
        self.paintShadow.setChecked(p)

    @QtCore.pyqtSignature("bool")
    def blockResizeCoord(self, pro):
        self.change[0].setEnabled(not pro)
        self.change[1].setEnabled(not pro)
        self.change[2].setEnabled(not pro)

    @QtCore.pyqtSignature("bool")
    def itemsPro(self, pro):
        #self.carSys.projectType = pro
        self.shape.projectType = pro
        self.updateAll()

    @QtCore.pyqtSignature("bool")
    def invisibility(self, i):
        self.shape.invis = i
        self.updateAll()

    def reDraw(self):
        self.shape.refresh()
        self.shape.resize()
        self.shape.rotate()
        self.shape.realloc()

        self.carSys.refresh()
        self.carSys.resize()
        self.carSys.rotate()
        self.carSys.realloc()
        self.updateAll()

    def shape_reBuild(self):
        self.shape.reBuild()
        self.reDraw()

    def updateAll(self):
        self.scene().update(self.carSys.scene().sceneRect())

    def carSysChangeColor(self):
        color = QtGui.QColorDialog.getColor(QtCore.Qt.black, self)
        if color.isValid():
            self.carSys.color = color

    def backGroundChangeColor(self):
        self.backcolor = QtGui.QColorDialog.getColor(QtCore.Qt.white, self)
        if self.backcolor.isValid():
            self.scene().setBackgroundBrush(QtGui.QBrush(self.backcolor))

    def backGroundChangePic(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, self.trUtf8("Виберіть зображення"), "./images",
                                                     self.trUtf8("Зображення (*.png *.jpg *.bmp)"))
        if fileName == '':
            return False
        try:
            self.scene().setBackgroundBrush(QtGui.QBrush(QtGui.QPixmap(fileName)))
        except:
            return False
        return True

    def backGroundChangeGrad(self):
        backcolor2 = QtGui.QColorDialog.getColor(QtCore.Qt.black, self)
        if backcolor2.isValid():
            self.backGroundSetGrad(backcolor2)

    def backGroundSetGrad(self, c):
        linearGrad = QtGui.QLinearGradient(-self.size().width() / 2, -self.size().height() / 2, self.size().width(),
                                           self.size().height())
        linearGrad.setColorAt(0, self.backcolor)
        linearGrad.setColorAt(1, c)
        self.scene().setBackgroundBrush(QtGui.QBrush(linearGrad))

    def scaleView(self, scaleFactor):
        factor = self.matrix().scale(scaleFactor, scaleFactor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()
        if factor < 0.07 or factor > 100:
            return
        self.scale(scaleFactor, scaleFactor)

    def mouseDoubleClickEvent(self, event):
        self.shape.refreshAll()
        self.carSys.refreshAll()
        self.updateAll()

    @QtCore.pyqtSignature("bool")
    def animate(self, state):
        if state:
            self.time1 = self.startTimer(50)
            self.time2 = self.startTimer(100)
            self.time3 = None
            self.i = 0
            self.b = 0
        self.animationIsEnable = state

    def timerEvent(self, event):
        if not self.animationIsEnable:
            return
        if event.timerId() == self.time1:
            self.shape.setRotY(-5)
            self.shape.setRotX(-1)
            self.shape.setShiftX(math.cos(self.i))
            self.shape.setShiftY(math.sin(self.i))
            self.shape.setShiftZ(10 * math.sin(self.i))
            self.i += 0.05
            if self.shape.numGen == -1:
                if self.b == 0:
                    self.time3 = self.startTimer(300)
                self.shape.setScaleX(1.5)
                self.shape.setScaleY(1.5)
                self.shape.setScaleZ(1.5)
                self.b = 1
        elif event.timerId() == self.time3:
            if self.shape.numGen == -1:
                event.accept()
                print 'Figure break activated'
                os._exit(1)
        self.reDraw()
        event.accept()

    def mousePressEvent(self, event):
        if (inside(self.carSys.boundingRect(), event.pos(),
                   QtCore.QPoint(self.size().width() / 2, self.size().height() / 2, ))):
            if event.buttons() == QtCore.Qt.RightButton:
                self.menuIn.exec_(QtGui.QCursor.pos())
            if event.buttons() == QtCore.Qt.LeftButton:
                self.mousePressed = True
                self.mousePressPos.setX(event.pos().x())
                self.mousePressPos.setY(event.pos().y())
                # print  self.mousePressPos.x()
                event.accept()
        else:
            if event.buttons() == QtCore.Qt.RightButton:
                self.menuOut.exec_(QtGui.QCursor.pos())

    def mouseMoveEvent(self, event):
        if self.mousePressed == True:
            if self.rotate.isChecked():
                self.carSys.setRotX((event.pos().x() - self.mousePressPos.x()) * 1.0)
                self.carSys.setRotY((event.pos().y() - self.mousePressPos.y()) * 1.0)

                self.shape.setRotX((event.pos().x() - self.mousePressPos.x()) * 1.0)
                self.shape.setRotY((event.pos().y() - self.mousePressPos.y()) * 1.0)

                self.mousePressPos.setX(event.pos().x())
                self.mousePressPos.setY(event.pos().y())
                self.reDraw()
                event.accept()
            else:
                self.carSys.setShiftX(self.shiftScale * (event.pos().x() - self.mousePressPos.x()) * 1.0)
                self.carSys.setShiftY(self.shiftScale * (event.pos().y() - self.mousePressPos.y()) * 1.0)

                self.shape.setShiftX(self.shiftScale * (event.pos().x() - self.mousePressPos.x()) * 1.0)
                self.shape.setShiftY(self.shiftScale * (event.pos().y() - self.mousePressPos.y()) * 1.0)

                self.mousePressPos.setX(event.pos().x())
                self.mousePressPos.setY(event.pos().y())
                self.reDraw()
                event.accept()

    def mouseReleaseEvent(self, event):
        self.mousePressed = False

    def itemMoved(self):
        if not self.timerId:
            self.timerId = self.startTimer(1000 / 25)

    def keyPressEvent(self, event):
        key = event.key()
        key_n = event.nativeModifiers()

        def keyAll(k):
            return key_n == k or key == k

        mod = event.modifiers()
        dRotate = 5
        dShift = 2
        if mod == QtCore.Qt.ShiftModifier:
            if key == QtCore.Qt.Key_Up:
                self.carSys.setRotX(dRotate)
                self.shape.setRotX(dRotate)
            elif key == QtCore.Qt.Key_Down:
                self.carSys.setRotX(-dRotate)
                self.shape.setRotX(-dRotate)

            elif key == QtCore.Qt.Key_Left:
                self.carSys.setRotY(dRotate)
                self.shape.setRotY(dRotate)

            elif key == QtCore.Qt.Key_Right:
                self.carSys.setRotY(-dRotate)
                self.shape.setRotY(-dRotate)

            elif key == QtCore.Qt.Key_Plus:
                pass;
            elif key == QtCore.Qt.Key_Minus:
                pass;
            elif key == QtCore.Qt.Key_Space or key == QtCore.Qt.Key_Enter:
                self.shape.refreshAll()
                self.carSys.refreshAll()
                self.updateAll()
            else:
                QtGui.QGraphicsView.keyPressEvent(self, event)

        elif mod == QtCore.Qt.ControlModifier:
            if keyAll(QtCore.Qt.Key_W) or key == QtCore.Qt.Key_Up:
                self.carSys.setShiftZ(-dShift)
                self.shape.setShiftZ(-dShift)
            elif keyAll(QtCore.Qt.Key_S) or key == QtCore.Qt.Key_Down:
                self.carSys.setShiftZ(dShift)
                self.shape.setShiftZ(dShift)
        else:
            if keyAll(QtCore.Qt.Key_W) or key == QtCore.Qt.Key_Up:
                self.carSys.setShiftY(-dShift)
                self.shape.setShiftY(-dShift)
            elif keyAll(QtCore.Qt.Key_S) or key == QtCore.Qt.Key_Down:
                self.carSys.setShiftY(dShift)
                self.shape.setShiftY(dShift)

            elif keyAll(QtCore.Qt.Key_A) or key == QtCore.Qt.Key_Left:
                self.carSys.setShiftX(-dShift)
                self.shape.setShiftX(-dShift)

            elif keyAll(QtCore.Qt.Key_D) or key == QtCore.Qt.Key_Right:
                self.carSys.setShiftX(dShift)
                self.shape.setShiftX(dShift)

            elif key == QtCore.Qt.Key_Escape:
                # self.shape.setScaleX(2);
                # self.shape.setScaleY(2);
                # self.shape.setScaleZ(2);
                self.shape.numGen = -1
                self.shape_reBuild()
            elif key == QtCore.Qt.Key_Minus:
                pass;
            elif key == QtCore.Qt.Key_Space or key == QtCore.Qt.Key_Enter:
                self.shape.refreshAll()
                self.carSys.refreshAll()
                self.updateAll()
            else:
                QtGui.QGraphicsView.keyPressEvent(self, event)
        # print    event.text()
        self.reDraw()

    def wheelEvent(self, event):
        dRotate = 5
        dScale = 0.1
        if (not inside(self.carSys.boundingRect(), event.pos(),
                       QtCore.QPoint(self.size().width() / 2, self.size().height() / 2, ))):
            if event.delta() > 0:
                if self.changeOut[0].isChecked():
                    self.carSys.setScaleX(+ dScale)
                if self.changeOut[1].isChecked():
                    self.carSys.setScaleY(+ dScale)
                if self.changeOut[2].isChecked():
                    self.carSys.setScaleZ(+ dScale)
            if event.delta() < 0:
                if self.changeOut[0].isChecked():
                    self.carSys.setScaleX(- dScale)
                if self.changeOut[1].isChecked():
                    self.carSys.setScaleY(- dScale)
                if self.changeOut[2].isChecked():
                    self.carSys.setScaleZ(- dScale)
        if self.rotate.isChecked():
            if (inside(self.carSys.boundingRect(), event.pos(),
                       QtCore.QPoint(self.size().width() / 2, self.size().height() / 2))):
                if event.delta() > 0:
                    self.carSys.setRotZ(+ dRotate)
                    self.shape.setRotZ(+ dRotate)
                else:
                    self.carSys.setRotZ(- dRotate)
                    self.shape.setRotZ(- dRotate)
                self.reDraw()

        if not self.rotate.isChecked():
            if (inside(self.carSys.boundingRect(), event.pos(),
                       QtCore.QPoint(self.size().width() / 2, self.size().height() / 2))):
                if event.delta() > 0:
                    if self.change[0].isChecked():
                        self.shape.setScaleX(+ dScale)
                    if self.change[1].isChecked():
                        self.shape.setScaleY(+ dScale)
                    if self.change[2].isChecked():
                        self.shape.setScaleZ(+ dScale)
                if event.delta() < 0:
                    if self.change[0].isChecked():
                        self.shape.setScaleX(- dScale)
                    if self.change[1].isChecked():
                        self.shape.setScaleY(- dScale)
                    if self.change[2].isChecked():
                        self.shape.setScaleZ(- dScale)

        self.reDraw()

    def itemMoved(self):
        if not self.timerId:
            self.timerId = self.startTimer(1000 / 25)

# ----------------------------------------------------------------------------
