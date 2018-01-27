import sys


debug = __debug__ 
debug = False

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
		
