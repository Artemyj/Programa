#! /usr/bin/env python
# -*- coding: utf-8 -*-

import math

from PyQt4 import QtCore, QtGui

from point3d import * 
from matrix  import * 
from side  import * 


def mulPi(i):
        i =  math.pi*i
        return i

class Plane(QtGui.QGraphicsItem):

        Type = QtGui.QGraphicsItem.UserType + 1
                
        def __init__ (self, x = 0, y =210 , z = 0 , r = 300,  parent = None):
                        QtGui.QGraphicsItem.__init__(self, parent)
                        self.R = r
                        self.nodes = [None , None, None, None]
                        self.projectType = 0;
                        self.nodes[0] = Point3d( x + self.R, y , z  +  self.R)
                        self.nodes[1] = Point3d( x + self.R, y , z - self.R)
                        self.nodes[2] = Point3d( x - self.R, y , z - self.R)
                        self.nodes[3] = Point3d( x - self.R, y , z + self.R)
                        
        def toPath(self):
                man = self.projectType 
                path= QtGui.QPainterPath()
                for i in xrange(4):
                        path.moveTo(self.nodes[i].toQPointF(man));
                        path.lineTo(self.nodes[i].toQPointF(man));      
                return path 

        def toQPolygonF(self, man = 0):
                points = [];
                for node in  self.nodes:
                        points.append(node.toQPointF(man));
                return QtGui.QPolygonF(points);
                        
        def boundingRect(self) :
                return self.toPath().boundingRect();
             
        def paint(self, painter, option, widget):
               zX = []
               for node in self.nodes:
                         zX .append(node.z)        
               zNum = max(zX) / len(self.nodes);       
               self.setZValue ( zNum);
               painter.setPen(QtGui.QPen(QtCore.Qt.black))
               painter.setBrush(QtGui.QBrush(QtCore.Qt.white))
               painter.drawPolygon(self.toQPolygonF(self.projectType) )
                                
                                       
#--------------------------------------------------------------------------------        
# class PlaneS(QtGui.QGraphicsItem):

        # Type = QtGui.QGraphicsItem.UserType + 1
                
        # def __init__ (self):
                        # QtGui.QGraphicsItem.__init__(self)
                        # self.sides = []
                        # self.R = 200
                        # self.sidesNum = 20
                        # self.projectType  = 0;
                        
                        # for i in xrange( self.sidesNum  ):
                          # for j in xrange( self.sidesNum  ):
                               # side = PlaneSide( i*20 - 200, 210 ,j*20 , 10, self)
                               # self.sides.append(side)

        # def toPath(self):
                # man = self.projectType 
                # path= QtGui.QPainterPath()
                
               
                # return path 
                
        # def boundingRect(self) :
                # return self.toPath().boundingRect();
             
        # def paint(self, painter, option, widget):
               # for side in self.sides:
                        # side.projectType  = self.projectType 
                        # side.paint( painter, option, widget);