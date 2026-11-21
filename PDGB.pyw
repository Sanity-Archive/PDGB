
import sys
from pathlib import Path

from PyQt6.QtCore import QUrl, Qt, QStandardPaths
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QSplitter,
    QMessageBox
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage
from PyQt6.QtGui import QShortcut, QKeySequence


APP_NAME = "PDGBrowser"
GAME_URL = "https://universe.flyff.com/play"


class MainWindow(QWidget):
    def closeEvent(self, event):
        for browser in self.findChildren(QWebEngineView):
            browser.stop()
            browser.setPage(None)
            browser.deleteLater()

        event.accept()


app = QApplication(sys.argv)
app.setApplicationName(APP_NAME)
app.setQuitOnLastWindowClosed(True)


# Ask which mode to use before opening the browser
choice = QMessageBox()
choice.setWindowTitle("PDGBrowser")
choice.setText("How many screens do you want to play with?")

one_button = choice.addButton(
    "1 Screen", QMessageBox.ButtonRole.AcceptRole
)
two_button = choice.addButton(
    "2 Screens", QMessageBox.ButtonRole.AcceptRole
)

choice.setDefaultButton(two_button)
choice.exec()

if choice.clickedButton() not in (one_button, two_button):
    sys.exit(0)

screen_count = 1 if choice.clickedButton() == one_button else 2


window = MainWindow()
layout = QVBoxLayout(window)
layout.setContentsMargins(0, 0, 0, 0)


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

    return view


# Create browser panels
left = create_browser("left_panel", GAME_URL)
right = None

if screen_count == 2:
    right = create_browser("right_panel", GAME_URL)


def toggleFS():
    if window.isFullScreen():
        window.showNormal()
    else:
        window.showFullScreen()


def reload_activePanel():
    focused_widget = QApplication.focusWidget()

    if screen_count == 1:
        left.reload()
        return

    if focused_widget is None:
        return

    if left is focused_widget or left.isAncestorOf(focused_widget):
        left.reload()
    elif right is not None and (
        right is focused_widget or right.isAncestorOf(focused_widget)
    ):
        right.reload()


shortcut = QShortcut(QKeySequence("CTRL+Ü"), window)
shortcut.activated.connect(toggleFS)

reload_shortcut = QShortcut(QKeySequence("CTRL+L"), window)
reload_shortcut.activated.connect(reload_activePanel)


# Build layout depending on selected mode
left.enterEvent = lambda event: left.setFocus()

if screen_count == 2:
    splitter = QSplitter(Qt.Orientation.Horizontal)

    right.enterEvent = lambda event: right.setFocus()

    splitter.addWidget(left)
    splitter.addWidget(right)

    layout.addWidget(splitter)
else:
    # Single browser, no splitter
    layout.addWidget(left)


window.showFullScreen()

sys.exit(app.exec())
