import sys
from PyQt5.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)
window = QWidget()
window.setGeometry(0, 0, 500, 300)
window.setWindowTitle("Dummy PyQt file")
window.show()
app.exec_()