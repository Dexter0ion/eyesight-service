from PyQt5.QtWidgets import QListView, QListWidget, QListWidgetItem
from PyQt5.QtCore import *

from PyQt5.QtGui import QIcon

import os
from PIL import Image


class QObjectList(QListWidget):
    def __init__(self):
        super().__init__()
        self.setViewMode(QListView.IconMode)
        self.setIconSize(QSize(200, 200))  #Icon 大小
        self.setMovement(QListView.Static)  #Listview显示状态
        #self.listWidget.setMaximumWidth(1000)  # 最大宽度
        self.setSpacing(5)  # 间距大小
        self.itemDoubleClicked.connect(self.displayItem)
        self.loadDataSource()

    def loadDataSource(self):
        names = []
        for i in os.listdir(r"./objectdatas"):
            names.append("./objectdatas" + "/" + i)

        for name in names:
            predItem = QListWidgetItem(self)
            predItem.setIcon(QIcon(name))
            predItem.setText(name[14:-4])
            #predItem.setTextAlignment(Qt.AlignHCenter)
            predItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
    
    def reloadDataSource(self):
        self.clear()

        self.loadDataSource()
    def displayItem(self,item):
        itemText = item.text()
        filename = itemText+'.jpg'
        print(filename)
        filepath = './objectdatas/'+filename

        img=Image.open(filepath)
        img.show()