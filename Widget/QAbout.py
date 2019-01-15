from PyQt5.QtWidgets import QDialog
class QAbout(QDialog):
    def __init__(self,parent):
        super().__init__(parent)
        self.resize(300, 300)
