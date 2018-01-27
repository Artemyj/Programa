
import sys
import src3d
import PyQt4


if __name__ == '__main__':
        try:
                app = PyQt4.QtGui.QApplication([sys.argv[0],"-style","plastique"]);
                window = src3d.MainWindow(  src3d.Graphic() );
                window.show();
                app.exec_();
        except:
                pass;
