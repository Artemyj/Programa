

from PyQt4 import QtCore, QtGui, uic

import xml

import config
from PerspectiveParams import PerspectiveParam

ui = config.configUi()



class AboutDialog(QtGui.QDialog):
    def __init__(self, *args):
        QtGui.QDialog.__init__(self, *args)
        uic.loadUi(ui[1], self)


class HelpDialog(QtGui.QDialog):
    def __init__(self, *args):
        QtGui.QDialog.__init__(self, *args)
        uic.loadUi(ui[2], self)


# ******************************************************************************


class MainWindow(QtGui.QMainWindow):
    def __init__(self, engin, *args):
        QtGui.QMainWindow.__init__(self, *args)
        uic.loadUi(ui[0], self)
        self.aboutDialog = AboutDialog(self)
        self.helpDialog = HelpDialog(self)
        self.view = engin
        self.paintScrollArea.setWidget(self.view)

        self.join = False

        self.checkConnections()
        self.commonConnections()
        self.init()

    def init(self):

        self.view.shape.tFromSlot(self.tFrom.value())
        self.view.shape.hFromSlot(self.hFrom.value())
        self.view.shape.tToSlot(self.tTo.value())
        self.view.shape.hToSlot(self.hTo.value())
        self.view.shape.tStepSlot(self.stepDoubleSpinBoxT.value())
        self.view.shape.hStepSlot(self.stepDoubleSpinBoxH.value())
        self.view.shape.funcX = self.funcXlineEdit.text()
        self.view.shape.funcY = self.funcYlineEdit.text()
        self.view.shape.funcZ = self.funcZlineEdit.text()
        self.view.shape_reBuild()

        self.setColor1(QtGui.QColor(0, 0, 127))
        self.setColor2(QtGui.QColor(255, 255, 255))
        self.setColor3(QtGui.QColor(255, 255, 127))

        self.paintingNumsChange()
        self.lampXYZ()

        self.view.animate(True)
        self.setLightMode(2)

    def checkConnections(self):
        self.connect(self.tFrom, QtCore.SIGNAL("valueChanged(double)"), self.tTo_setMinimum)
        self.connect(self.hFrom, QtCore.SIGNAL("valueChanged(double)"), self.hTo_setMinimum)
        self.connect(self.hTo, QtCore.SIGNAL("valueChanged(double)"), self.hFrom_setMaximum)
        self.connect(self.tTo, QtCore.SIGNAL("valueChanged(double)"), self.tFrom_setMaximum)

        self.connect(self.stepPushButton, QtCore.SIGNAL("clicked()"), self.joinSteps)

    def commonConnections(self):

        self.view.shape.funcAll = self.plainTextEdit.toPlainText()
        self.connect(self.actionNorm, QtCore.SIGNAL("triggered( bool )"), self.showNormals)
        self.connect(self.view.paintShadow, QtCore.SIGNAL("triggered( bool )"), self.actionShad.setChecked)
        self.connect(self.actionShad, QtCore.SIGNAL("triggered( bool )"), self.view.shadow)
        self.connect(self.actionPrint, QtCore.SIGNAL("triggered( bool )"), self.printView)
        self.connect(self.actioAnim, QtCore.SIGNAL("triggered( bool )"), self.view.animate)
        self.connect(self.actionFull_Screen, QtCore.SIGNAL("triggered( bool )"), self.fullScreen)
        self.connect(self.actionAbout_QT, QtCore.SIGNAL("triggered()"), QtGui.qApp, QtCore.SLOT("aboutQt()"))
        self.connect(self.actionAboutMe, QtCore.SIGNAL("triggered()"), self.aboutDialog.show)
        self.connect(self.actionHelp, QtCore.SIGNAL("triggered()"), self.helpDialog.show)
        self.connect(self.action_Axis, QtCore.SIGNAL("triggered(bool)"), self.view.carSys.setVisible)
        self.connect(self.action_Axis, QtCore.SIGNAL("triggered(bool)"), self.view.ac.setEnabled)
        self.connect(self.tFrom, QtCore.SIGNAL("valueChanged(double)"), self.view.shape.tFromSlot)
        self.connect(self.tTo, QtCore.SIGNAL("valueChanged(double)"), self.view.shape.tToSlot)
        self.connect(self.hFrom, QtCore.SIGNAL("valueChanged(double)"), self.view.shape.hFromSlot)
        self.connect(self.hTo, QtCore.SIGNAL("valueChanged(double)"), self.view.shape.hToSlot)

        self.connect(self.stepDoubleSpinBoxT, QtCore.SIGNAL("valueChanged(int)"), self.view.shape.tStepSlot)
        self.connect(self.stepDoubleSpinBoxH, QtCore.SIGNAL("valueChanged(int)"), self.view.shape.hStepSlot)

        self.connect(self.funcXlineEdit, QtCore.SIGNAL("editingFinished()"), self.setFuncX)
        self.connect(self.funcYlineEdit, QtCore.SIGNAL("editingFinished() "), self.setFuncY)
        self.connect(self.funcZlineEdit, QtCore.SIGNAL("editingFinished()"), self.setFuncZ)
        self.connect(self.plainTextEdit, QtCore.SIGNAL("textChanged()"), self.setScript)

        self.connect(self.tFrom, QtCore.SIGNAL("valueChanged(double)"), self.view.shape_reBuild)
        self.connect(self.tTo, QtCore.SIGNAL("valueChanged(double)"), self.view.shape_reBuild)
        self.connect(self.hFrom, QtCore.SIGNAL("valueChanged(double)"), self.view.shape_reBuild)
        self.connect(self.hTo, QtCore.SIGNAL("valueChanged(double)"), self.view.shape_reBuild)
        self.connect(self.stepDoubleSpinBoxT, QtCore.SIGNAL("valueChanged(int)"), self.view.shape_reBuild)
        self.connect(self.stepDoubleSpinBoxH, QtCore.SIGNAL("valueChanged(int)"), self.view.shape_reBuild)


        self.connect(self.funcXlineEdit, QtCore.SIGNAL("editingFinished()"), self.view.shape_reBuild)
        self.connect(self.funcYlineEdit, QtCore.SIGNAL("editingFinished() "), self.view.shape_reBuild)
        self.connect(self.funcZlineEdit, QtCore.SIGNAL("editingFinished()"), self.view.shape_reBuild)
        self.connect(self.plainTextEdit, QtCore.SIGNAL("textChanged()"), self.view.shape_reBuild)

        self.connect(self.funcXlineEdit, QtCore.SIGNAL("editingFinished()"), self.view.updateAll)
        self.connect(self.funcYlineEdit, QtCore.SIGNAL("editingFinished() "), self.view.updateAll)
        self.connect(self.funcZlineEdit, QtCore.SIGNAL("editingFinished()"), self.view.updateAll)
        self.connect(self.plainTextEdit, QtCore.SIGNAL("textChanged()"), self.view.updateAll)

        self.connect(self.tFrom, QtCore.SIGNAL("valueChanged(double)"), self.view.updateAll)
        self.connect(self.tTo, QtCore.SIGNAL("valueChanged(double)"), self.view.updateAll)
        self.connect(self.hFrom, QtCore.SIGNAL("valueChanged(double)"), self.view.updateAll)
        self.connect(self.hTo, QtCore.SIGNAL("valueChanged(double)"), self.view.updateAll)

        self.connect(self.stepDoubleSpinBoxT, QtCore.SIGNAL("valueChanged(int)"), self.view.updateAll)
        self.connect(self.stepDoubleSpinBoxH, QtCore.SIGNAL("valueChanged(int)"), self.view.updateAll)

        self.connect(self.genCheckBox, QtCore.SIGNAL("stateChanged(int)"), self.changeShapeGen)
        self.connect(self.cb_parallel, QtCore.SIGNAL("stateChanged(int)"), self.setLightMode)

        self.connect(self.intenDoubleSpinBox, QtCore.SIGNAL("valueChanged(double)"), self.paintingNumsChange)
        self.connect(self.difDoubleSpinBox, QtCore.SIGNAL("valueChanged(double)"), self.paintingNumsChange)
        self.connect(self.mirrDoubleSpinBox, QtCore.SIGNAL("valueChanged(double)"), self.paintingNumsChange)

        self.connect(self.sb_light_x, QtCore.SIGNAL("valueChanged(double)"), self.lampXYZ)
        self.connect(self.sb_light_y, QtCore.SIGNAL("valueChanged(double)"), self.lampXYZ)
        self.connect(self.sb_light_z, QtCore.SIGNAL("valueChanged(double)"), self.lampXYZ)

        self.connect(self.sb_wall, QtCore.SIGNAL("valueChanged(double)"), self.setWall)

        self.connect(self.powSpinBox, QtCore.SIGNAL("valueChanged(int)"), self.paintingNumsChange)
        self.connect(self.aLphaSpinBox, QtCore.SIGNAL("valueChanged(int)"), self.alphaChange)
        self.connect(self.aLphaSpinBox_2, QtCore.SIGNAL("valueChanged(int)"), self.alphaChange)

        self.connect(self.colorButton1, QtCore.SIGNAL("clicked()"), self.selectColor1)
        self.connect(self.colorButton2, QtCore.SIGNAL("clicked()"), self.selectColor2)
        self.connect(self.colorButton3, QtCore.SIGNAL("clicked()"), self.selectColor3)

        self.connect(self.radioButton1, QtCore.SIGNAL("clicked(bool)"), self.selectMethod)
        self.connect(self.radioButton2, QtCore.SIGNAL("clicked(bool)"), self.selectMethod)

        self.connect(self.z0, QtCore.SIGNAL("valueChanged(int)"), self.changez0)
        self.connect(self.z1, QtCore.SIGNAL("valueChanged(int)"), self.changez1)

    def selectMethod(self):
        self.view.shape.type = self.radioButton2.isChecked()


    def changez0(self):
        PerspectiveParam.z0 = self.z0.value()

    def changez1(self):
        PerspectiveParam.z1 = self.z1.value()

    @QtCore.pyqtSignature("")
    def printView(self):
        self.view.printView()

    @QtCore.pyqtSignature("double")
    def setWall(self, p):
        self.view.shape.wall = p

    def alphaChange(self):
        self.view.shape.alpha = self.aLphaSpinBox.value()
        self.view.shape.alphaShadow = self.aLphaSpinBox_2.value()

    @QtCore.pyqtSignature("int")
    def setLightMode(self, p):
        self.view.shape.paral = p

    def lampXYZ(self):
        self.view.shape.lamp.x = self.sb_light_x.value()
        self.view.shape.lamp.y = self.sb_light_y.value()
        self.view.shape.lamp.z = self.sb_light_z.value()
        self.view.updateAll()

    def showNormals(self, p):
        pass;
        self.view.shape.showNormals = p
        self.view.updateAll()

    @QtCore.pyqtSignature("int")
    def changeShapeGen(self, p):
        self.view.shape.numGen = p
        self.view.shape_reBuild()

    @QtCore.pyqtSignature("")
    def paintingNumsChange(self):
        self.view.shape.inten = self.intenDoubleSpinBox.value()
        self.view.shape.defRefl = self.difDoubleSpinBox.value()
        self.view.shape.mirRefl = self.mirrDoubleSpinBox.value()
        self.view.shape.mirPow = self.powSpinBox.value()
        self.view.updateAll()

    def selectColor1(self):
        color = QtGui.QColorDialog.getColor(QtGui.QColor(0, 0, 127), self)
        self.setColor1(color)

    @QtCore.pyqtSignature("")
    def selectColor2(self):
        color = QtGui.QColorDialog.getColor(QtCore.Qt.white, self)
        self.setColor2(color)

    def selectColor3(self):
        color = QtGui.QColorDialog.getColor(QtCore.Qt.yellow, self)
        self.setColor3(color)

    def setColor1(self, c):
        if c.isValid():  # "#00ff00"
            self.view.shape.colorObj = c
            self.colorButton1.setPalette(QtGui.QPalette(c))
            self.colorButton1.setAutoFillBackground(1)
            self.view.updateAll()

    def setColor2(self, c):
        if c.isValid():
            self.view.shape.colorRlight = c
            self.colorButton2.setPalette(QtGui.QPalette(c))
            self.colorButton2.setAutoFillBackground(1)
            self.view.updateAll()

    def setColor3(self, c):
        if c.isValid():
            self.view.shape.colorLight = c
            self.colorButton3.setPalette(QtGui.QPalette(c))
            self.colorButton3.setAutoFillBackground(1)
            self.view.updateAll()

    @QtCore.pyqtSignature("")
    def joinSteps(self):
        if (self.join == False):
            self.stepDoubleSpinBoxH.setPrefix("= pi / ")
            self.stepDoubleSpinBoxH.setValue(self.stepDoubleSpinBoxT.value())
            self.connect(self.stepDoubleSpinBoxT, QtCore.SIGNAL("valueChanged(int)"), self.stepDoubleSpinBoxH.setValue)
            self.connect(self.stepDoubleSpinBoxH, QtCore.SIGNAL("valueChanged(int)"), self.stepDoubleSpinBoxT.setValue)
            self.join = True

        elif (self.join == True):
            self.stepDoubleSpinBoxH.setPrefix("pi / ")
            self.disconnect(self.stepDoubleSpinBoxT, QtCore.SIGNAL("valueChanged(int)"),
                            self.stepDoubleSpinBoxH.setValue)
            self.disconnect(self.stepDoubleSpinBoxH, QtCore.SIGNAL("valueChanged(int)"),
                            self.stepDoubleSpinBoxT.setValue)

            self.join = False

    @QtCore.pyqtSignature("double")
    def tTo_setMinimum(self, x):
        self.tTo.setMinimum(x)

    @QtCore.pyqtSignature("double")
    def hTo_setMinimum(self, x):
        self.hTo.setMinimum(x)

    @QtCore.pyqtSignature("double")
    def hFrom_setMaximum(self, x):
        self.hFrom.setMaximum(x)

    @QtCore.pyqtSignature("double")
    def tFrom_setMaximum(self, x):
        self.tFrom.setMaximum(x)

    @QtCore.pyqtSignature("")
    def setFuncX(self):
        self.view.shape.funcX = self.funcXlineEdit.text()

    @QtCore.pyqtSignature("")
    def setFuncY(self):
        self.view.shape.funcY = self.funcYlineEdit.text()

    @QtCore.pyqtSignature("")
    def setFuncZ(self):
        self.view.shape.funcZ = self.funcZlineEdit.text()

    @QtCore.pyqtSignature("")
    def setScript(self):
        self.view.shape.funcAll = self.plainTextEdit.toPlainText()

    @QtCore.pyqtSignature("bool")
    def fullScreen(self, state):
        if (state):
            self.showFullScreen()
        else:
            self.showNormal()

    def closeEvent(self, event):
        for i in xrange(1000):
            self.setGeometry(QtCore.QRect(i + self.x(), i + self.y(), -i * 10, -i * 10))

    def showEvent(self, event):
        pass;
