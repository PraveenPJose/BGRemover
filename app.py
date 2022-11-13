""" THIS IS A PYTHON APP FOR REMOVE BACKGROUND """

import sys, os
from pathlib import Path
import shutil

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap,QIcon
from rembg import remove
from PIL import Image

home = os.getenv("U2NET_HOME", os.path.join("~", ".u2net"))
path = Path(home).expanduser() / f"u2net.onnx"
path.parents[0].mkdir(parents=True, exist_ok=True)



if not path.exists():
    my_file = Path("u2net.onnx")
    if my_file.is_file():
        shutil.move('u2net.onnx', path)

class ImageLable(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop Image Here \n\n')
        self.setStyleSheet('''
            QLable{
                border: 4px dashed #aaa
            }
        ''')

    def setPixmap(self, image):
        resizedImage = image.scaled(400, 400, Qt.KeepAspectRatio)
        return super().setPixmap(resizedImage)   
         


class BGRemoverApp(QWidget):
    def __init__(self,):
        super().__init__()
        self.resize(400,400)
        self.setAcceptDrops(True)

        mainLayout = QVBoxLayout()

        self.photoViewer = ImageLable()
        mainLayout.addWidget(self.photoViewer)

        self.setLayout(mainLayout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()
    
    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            fileCount=len(event.mimeData().urls())
            i=0

            while i < fileCount:
                file_path = event.mimeData().urls()[i].toLocalFile()
                self.set_image(file_path)
                input = Image.open(file_path)
                output = remove(input)
                outputPath = self.get_save_image_path(file_path)
                output.save(outputPath)
                self.set_image(outputPath)
                i=i+1

            event.accept()
        else:
            event.ignore()

    def set_image(self,file_path):
        self.photoViewer.setPixmap(QPixmap(file_path))
    
    def get_save_image_path(self,file_path):
        fileArray= file_path.split("/")
        fileName=fileArray[-1]
        fileNameSplit= fileName.split(".")
        newFileName=fileName.replace("."+fileNameSplit[-1], "_bg.png")
        outPutFilePath=file_path.replace(fileName, newFileName)
        return outPutFilePath


app = QApplication(sys.argv)
myApp=BGRemoverApp()
myApp.setWindowTitle('BG Remover')
myApp.setWindowIcon(QIcon('icon.png'))

myApp.show()
sys.exit(app.exec_())