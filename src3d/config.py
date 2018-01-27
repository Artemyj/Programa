
import os
import os.path
import ConfigParser
import sys



_uiMainWindow = "ui/Window.ui";
_uiAboutDialog  = "ui/About.ui";
_uiHelpDialog  = "ui/Man.ui";
ConfIni = "config.ini"

def _errorUi(str):
	print "No such Ui: %s"%(str)
	sys.exit(0)

def _check(str):
		if( os.path.isfile(str) == 0 ):
			_errorUi(str);
	
def _default():
	uiMainWindow = os.path.normcase(_uiMainWindow)
	uiAboutDialog = os.path.normcase(_uiAboutDialog)
	uiHelpDialog = os.path.normcase(_uiHelpDialog)
	if( os.path.isfile(uiMainWindow) == 0 ):
		uiMainWindow = "Window.ui"
		uiMainWindow = os.path.normcase(uiMainWindow)
		_check(uiMainWindow)
	if( os.path.isfile(uiAboutDialog) == 0 ):
		uiAboutDialog = "About..ui"
		uiAboutDialog = os.path.normcase(uiAboutDialog)
		_check(uiAboutDialog)
	return [uiMainWindow, uiAboutDialog, uiHelpDialog]

def configUi():
	if( os.path.isfile(ConfIni) != 0 ):
		ConfigINI = open(ConfIni, "r");
		config_parser = ConfigParser.ConfigParser();
		config_parser.read(ConfIni);
		try:
			uiMainWindow = config_parser.get('uifiles','mainwindow');
			uiAboutDialog = config_parser.get('uifiles','aboutwindow');
			uiHelpDialog = config_parser.get('uifiles','helpwindow');
			uiMainWindow = os.path.normcase(uiMainWindow)
			uiAboutDialog = os.path.normcase(uiAboutDialog)  
			_check(uiMainWindow)
			_check(uiAboutDialog)
			return [uiMainWindow, uiAboutDialog,uiHelpDialog]
		except:	
			print "WRONG CONFIG!\n"
			return _default()
	else:
		return _default()
	

