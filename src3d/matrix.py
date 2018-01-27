
from types import * 
from point3d import * 

class Matrix:
      def __init__(self, n, m):
        self.n = n
        self.m = m
        self.vec = []
        for i in xrange(n):
          self.vec.append([])
          for j in xrange(m):
            self.vec[i].append(0)

      def toPoint(self):
        if( (self.n == 4 ) and (self.m == 1 )):
                point = Point (self.vec[0][0]/ self.vec[3][0], self.vec[1][0]/ self.vec[3][0],self.vec[2][0]/ self.vec[3][0])
        else :
              raise TypeError("def toPoint(self): if( (self.n == 4 ) and (self.m == 1 )):")

      def null(self):
          for i in xrange(self.n):
                for j in xrange(self.m):
                        self.vec[i][j] = 0

      def unit(self):
          for i in xrange(self.n):
                for j in xrange(self.m):
                        if(i == j):
                                self.vec[i][j] = 1
                        else :
                                self.vec[i][j] = 0

      def unitDiag(self):
          for i in xrange(self.n):
                for j in xrange(self.m):
                        if(i == j):
                                self.vec[i][j] = 1

      def unitDiag2(self):
          for i in xrange(self.n):
                for j in xrange(self.m):
                        if(i == j):
                                self.vec[i][j] = -1

      def diag(self, a):
          for i in xrange(self.n):
                for j in xrange(self.m):
                        if(i == j):
                                self.vec[i][j] = a

      def __neg__(self):
          for i in xrange(self.n):
                for j in xrange(self.m):
                                self.vec[i][j] = -self.vec[i][j]

      def unitButLast(self):
          for i in xrange(self.n - 1):
                for j in xrange(self.m - 1):
                        if i == j:
                                self.vec[i][j] = 1

      def copy(self):
        res = Matrix(self.n,  self.m)
        for i in xrange(self.n):
          for j in xrange(self.m):
            res.vec[i][j] = self.vec[i][j]
        return res

      def __getitem__(self, i):
        if ((type(i) is IntType)
        or (type(i) is LongType)
        and (i < self.n)):
              return self.vec[i]
        else :
              raise IndexError("Matrix.__getitem__(self, Long or IntType < n)")

      def __setitem__(self, i, value):
        if ((type(i) is IntType)
        or (type(i) is LongType)) \
        and ( (type(value) is ListType)
        and (i < self.n)
        and (len(value) == self.m)):   
              self.vec[i] = value
        else :
              raise IndexError("Matrix.__setitem__(self, Long or IntType < n, value == m)")

      def __mul__(self, other):
          a = Matrix(self.n , other.m)
          if( other.n != self.m  ):
                return a
          buff = 0.0
          for i in xrange(a.n):
                for j in xrange(a.m):
                      buff = 0.0
                      for k in xrange(self.m):
                        buff += self.vec[i][k]*other.vec[k][j]
                        a.vec[i][j] = buff
          return a


