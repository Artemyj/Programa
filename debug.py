﻿#!/usr/bin/env python
#?/usr/bin/env pythonw

import sys
import src3d
import PyQt4


'''
 *********************************************************************************
        D-E-B-U-G
*********************************************************************************
'''
if src3d.debug :
	print 'DEBUG'
pass;
'''
 *********************************************************************************
		M A I N
*********************************************************************************
'''

if __name__ == '__main__':
	app = PyQt4.QtGui.QApplication([sys.argv[0],"-style","plastique"]);
	window = src3d.MainWindow(  src3d.Graphic() );
	window.show();
	app.exec_();

