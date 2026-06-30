import sys

from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSplitter
from PyQt6.QtWebEngineWidgets import QWebEngineView

app = QApplication(sys.argv)

window = QWidget()
layout = QVBoxLayout(window)

splitter = QSplitter(Qt.Orientation.Horizontal)

left = QWebEngineView()
right = QWebEngineView()

left.setUrl(QUrl("https://universe.flyff.com/play"))
right.setUrl(QUrl("https://universe.flyff.com/play"))

left.enterEvent = lambda event: left.setFocus()
right.enterEvent = lambda event: right.setFocus()

splitter.addWidget(left)
splitter.addWidget(right)

layout.addWidget(splitter)



splitter.addWidget(left)
splitter.addWidget(right)


window.resize(1200, 800)
window.show()

sys.exit(app.exec())