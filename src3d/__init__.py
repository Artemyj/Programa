#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
try:
        from psyco  import * 
        full();
except:
        sys.stderr.write( "There is no PSYCO ! - It's very sad!\n")
                

debug = __debug__ 
debug = False;

if  debug :
	from carsys  import * 
	from shape  import * 
	from matrix  import * 	
	from point3d  import * 
	from engine  import * 
	from MainWindow  import * 
else:
	from engine  import * 
	from MainWindow  import * 
		
