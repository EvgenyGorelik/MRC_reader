from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import mrcfile 
import atexit
from io import StringIO
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from PIL import Image

class filedialogdemo(QWidget):
    def __init__(self, parent = None):
        super(filedialogdemo, self).__init__(parent)
            
        layout = QVBoxLayout()
        self.btn = QPushButton("Open .mrc")
        self.btn.clicked.connect(self.getfile)
        layout.addWidget(self.btn)

        self.fn = QLabel("No File Selected")
        layout.addWidget(self.fn)

        button_layout = QHBoxLayout()
        self.btn2 = QPushButton("Print Header")
        self.btn2.clicked.connect(self.print_header)
        self.btn2.setEnabled(False)
        button_layout.addWidget(self.btn2)

        self.btn3 = QPushButton("Print First Frame")
        self.btn3.clicked.connect(self.print_img)
        self.btn3.setEnabled(False)
        button_layout.addWidget(self.btn3)

        self.btn4 = QPushButton("Export All Frame")
        self.btn4.clicked.connect(self.export_all)
        self.btn4.setEnabled(False)
        button_layout.addWidget(self.btn4)

        layout.addLayout(button_layout)


        disp_layout = QHBoxLayout()
        self.consol = QTextEdit()
        disp_layout.addWidget(self.consol)

        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.subplots()
        self.ax.set_axis_off()
        disp_layout.addWidget(self.canvas)

        layout.addLayout(disp_layout)
        
        self.setLayout(layout)
        self.setWindowTitle("MRC File Reader")

        self.mrc_file = None

        sys.stdout = self.stdout = StringIO()

        atexit.register(self.cleanup)

    def cleanup(self):
        print("Running cleanup...")
        if self.mrc_file is not None:
            self.mrc_file.close()

            
    def getfile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 
            'c:\\',"MRC files (*.mrc)")
        if fname[0]:
            self.fn.setText(fname[0])
            self.mrc_file = mrcfile.open(fname[0], 'r')
            self.btn2.setEnabled(True)
            self.btn3.setEnabled(True)
            self.btn4.setEnabled(True)

    def print_header(self):
        self.mrc_file.print_header()
        self.consol.setText(self.stdout.getvalue())
        self.stdout.close()
        sys.stdout = self.stdout = StringIO()

        
    def print_img(self):
        self.ax.imshow(self.mrc_file.data[0])

    
    def export_all(self):
        dir = QFileDialog.getExistingDirectory(self, "Save Frames To...")
        for i, data in enumerate(self.mrc_file.data):
            Image.fromarray(data).save(dir + f"\\frame_{str(i).zfill(4)}.tif")


def main():
    app = QApplication(sys.argv)
    ex = filedialogdemo()
    ex.show()
    sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()