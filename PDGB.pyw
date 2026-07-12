import sys
from pathlib import Path

from PyQt6.QtCore import QUrl, Qt, QStandardPaths, qVersion
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSplitter
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage, QWebEngineSettings
from PyQt6.QtGui import QShortcut, QKeySequence


APP_NAME = "PDGBrowser"



class MainWindow(QWidget):
    def closeEvent(self, event):
        for browser in self.findChildren(QWebEngineView):
            browser.stop()
            browser.setPage(None)
            browser.deleteLater()
        
        event.accept()
        QApplication.quit()

app = QApplication(sys.argv)
app.setApplicationName(APP_NAME)
app.setQuitOnLastWindowClosed(True)


window = MainWindow()
layout = QVBoxLayout(window)

def create_browser(panel_name: str, url: str, parent=None) -> QWebEngineView:
    view = QWebEngineView(parent)

    base = Path(QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppDataLocation
    ))

    profile_dir = base / "profiles" / panel_name
    cache_dir = base / "cache" / panel_name

    profile_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    profile = QWebEngineProfile(panel_name, view)

    profile.setPersistentStoragePath(str(profile_dir))
    profile.setCachePath(str(cache_dir))
    profile.setPersistentCookiesPolicy(
        QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies
    )


    page = QWebEnginePage(profile, view)
    view.setPage(page)

    if url:
        view.load(QUrl(url))

    # view.profile = profile
    # view.web_page = page
    
    # view.setPage(page)
    # view.load(QUrl(url))


    return view

def toggleFS():
     if window.isFullScreen():
         window.showNormal()
     else:
         window.showFullScreen()

def reload_activePanel():
    focused_widget = QApplication.focusWidget()

    if focused_widget is None:
        return
    
    if ( focused_widget is left or left.isAncestorOf(focused_widget)):
        left.reload()
    elif (focused_widget is right or right.isAncestorOf(focused_widget)):
        right.reload()


shortcut = QShortcut(QKeySequence("CTRL+Ü"), window)
shortcut.activated.connect(toggleFS)

reload_shortcut = QShortcut(QKeySequence("CTRL+P"), window)
reload_shortcut.activated.connect(reload_activePanel)


splitter = QSplitter(Qt.Orientation.Horizontal)

# print("QT:", qVersion())
left = create_browser("left_panel", "https://universe.flyff.com/play")
right = create_browser("right_panel", "https://universe.flyff.com/play")

left.enterEvent = lambda event: left.setFocus()
right.enterEvent = lambda event: right.setFocus()

splitter.addWidget(left)
splitter.addWidget(right)

layout.addWidget(splitter)


window.showFullScreen()



sys.exit(app.exec())