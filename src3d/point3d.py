blackPoolZ = 1000

import PyQt4
import math
from types import *
from PerspectiveParams import PerspectiveParam


class Point3d:
    def __init__(self, x=0, y=0, z=0):
        if isinstance(x, ListType):
            self.x = x[0]
            self.y = x[1]
            self.z = x[2]
        elif isinstance(x,(int,long,float)):
            self.x = x
            self.y = y
            self.z = z
        else:
            raise TypeError("<<Point3d(x = 0 || [0,0,0], 0, 0)>>")
        self.t = 1

    def toList(self):
        return [self.x, self.y, self.z]

    def toList4(self):
        return [self.x, self.y, self.z, 1]

    def __getitem__(self, i):
        if ((type(i) is IntType)
                or (type(i) is LongType)):
            if i == 0:
                return self.x
            if i == 1:
                return self.y
            if i == 2:
                return self.z
        else:
            raise IndexError("Point3d.__getitem__(self, Long or IntType)")

    def __setitem__(self, i, value):
        if ((type(i) is IntType)
            or (type(i) is LongType)) \
                and ((type(value) is IntType)
                     or (type(value) is LongType)
                     or (type(value) is FloatType)):
            if i == 0:
                self.x = value
            if i == 1:
                self.y = value
            if i == 2:
                self.z = value
        else:
            raise IndexError("Point3d.__setitem__(self, Long or IntType, value)")

    def __cmp__(self, other):
        if (self.x == other.x) and (self.y == other.y) and (self.z == other.z):
            return 0
        return -1

    def __or__(self, other):
        return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)

    def __xor__(self, b):
        a = self
        return Point3d(a.y * b.z - a.z * b.y, a.x * b.z - a.z * b.x, a.x * b.y - a.y * b.x)

    def __add__(self, other):
        return Point3d((self.x + other.x), (self.y + other.y), (self.z + other.z))

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __sub__(self, other):
        return Point3d((self.x - other.x), (self.y - other.y), (self.z - other.z))

    def __mul__(self, other):  # DANG
        return Point3d((self.x * other), (self.y * other), (self.z * other))

    def __div__(self, other):  # DANG
        if other != 0:
            return Point3d((self.x / other), (self.y / other), (self.z / other))
        else:
            raise ValueError("__div__ by 'O' !!! ")
            # return 0

    def __abs__(self):
        return math.sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

    def __neg__(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z

    def __str__(self):
        return "(%s\t %s\t %s)T" % (self.x, self.y, self.z)

    def __repr__(self):
        return "<%s\t %s\t %s>T" % (self.x, self.y, self.z)

    def perspShift(self):
        Point = Point3d(0, 0, -blackPoolZ)
        self.x *= ((Point.z - self.z) / Point.z)
        self.y *= ((Point.z - self.z) / Point.z)

    def perspShift_r(self):
        Point = Point3d(0, 0, -blackPoolZ)
        return Point3d(
            (self.x * (Point.z - self.z) / Point.z),
            (self.y * (Point.z - self.z) / Point.z), self.z)

    def toQPointF(self, mann=0):
        if mann == 0:
            return PyQt4.QtCore.QPointF(self.x, self.y)
        if PerspectiveParam.odn:
            return PyQt4.QtCore.QPointF((PerspectiveParam.x1 + (self.x-PerspectiveParam.x1) * PerspectiveParam.z0 / (self.z + PerspectiveParam.z0)),
                                        (PerspectiveParam.y1 + (self.y-PerspectiveParam.y1) * PerspectiveParam.z0 / (self.z + PerspectiveParam.z0)))
        if PerspectiveParam.two:
            x=PerspectiveParam.x1 + ((self.x-PerspectiveParam.x1) * PerspectiveParam.z0 / (self.z + PerspectiveParam.z0))
            y=PerspectiveParam.y1 + ((self.y-PerspectiveParam.y1) * PerspectiveParam.z0 / (self.z + PerspectiveParam.z0))
            x1=PerspectiveParam.x2 + ((x-PerspectiveParam.x2) * PerspectiveParam.z1 / (self.z + PerspectiveParam.z1))
            y1 = PerspectiveParam.y2 + (
                        (y - PerspectiveParam.y2) * PerspectiveParam.z1 / (self.z + PerspectiveParam.z1))
            return PyQt4.QtCore.QPointF(x1,y1)
        if PerspectiveParam.three:
            x=PerspectiveParam.x1 + ((self.x-PerspectiveParam.x1) * PerspectiveParam.z0 / (self.z + PerspectiveParam.z0))
            y=PerspectiveParam.y1 + ((self.y-PerspectiveParam.y1) * PerspectiveParam.z0 / (self.z + PerspectiveParam.z0))
            x1=PerspectiveParam.x2 + ((x-PerspectiveParam.x2) * PerspectiveParam.z1 / (self.z + PerspectiveParam.z1))
            y1 = PerspectiveParam.y2 + (
                        (y - PerspectiveParam.y2) * PerspectiveParam.z1 / (self.z + PerspectiveParam.z1))
            x2=PerspectiveParam.x3 + ((x1-PerspectiveParam.x3) * PerspectiveParam.z2 / (self.z + PerspectiveParam.z2))
            y2=y1 = PerspectiveParam.y3 + (
                        (y1 - PerspectiveParam.y3) * PerspectiveParam.z2 / (self.z + PerspectiveParam.z2))
            return PyQt4.QtCore.QPointF(x2,y2)




    def affTr(self, a):
        x = self.x
        y = self.y
        z = self.z
        self.x = x * a[0][0] + y * a[0][1] + z * a[0][2] + a[0][3]
        self.y = x * a[1][0] + y * a[1][1] + z * a[1][2] + a[1][3]
        self.z = x * a[2][0] + y * a[2][1] + z * a[2][2] + a[2][3]
        self.t = x * a[3][0] + y * a[3][1] + z * a[3][2] + a[3][3]

    def affTr2(self, a):
        x = self.x
        y = self.y
        z = self.z
        res = Point3d()
        res.x = x * a[0][0] + y * a[0][1] + z * a[0][2] + a[0][3]
        res.y = x * a[1][0] + y * a[1][1] + z * a[1][2] + a[1][3]
        res.z = x * a[2][0] + y * a[2][1] + z * a[2][2] + a[2][3]
        return res

    def cos(self, other):
        return (self | other) / (abs(self) * abs(other))


def sum3d(List):
    res = Point3d()
    for i in List:
        res += i
    return res


def ColorToPoint(Color):
    return Point3d(Color.redF(), Color.greenF(), Color.blueF())


def norm(v):
    n = abs(v)
    if n == 0:
        return Point3d()
    v = v / n
    return v
