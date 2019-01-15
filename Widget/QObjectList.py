from PyQt5.QtWidgets import QListView,QListWidget,QListWidgetItem
from PyQt5.QtCore import *

from PyQt5.QtGui import QIcon

import os
class QObjectList(QListWidget):
    def __init__(self):
        super().__init__()
        self.setViewMode(QListView.IconMode)
        self.setIconSize(QSize(150, 100))  #Icon 大小
        self.setMovement(QListView.Static)  #Listview显示状态
        #self.listWidget.setMaximumWidth(1000)  # 最大宽度
        self.setSpacing(12)  # 间距大小
    
        self.loadDataSource()

    def loadDataSource(self):
        names=[]
        for i in os.listdir(r"./objectdatas"):
            names.append("./objectdatas"+"/"+i)
        
        for name in names:
            predItem = QListWidgetItem(self)
            predItem.setIcon(QIcon(name))
            predItem.setText(name[14:-4])
            #predItem.setTextAlignment(Qt.AlignHCenter)
            predItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)