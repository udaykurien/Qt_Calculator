import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget,
    QLabel, QVBoxLayout,
    QGridLayout, QMainWindow,
    QPushButton, QSizePolicy,
    QHBoxLayout,
)
from PyQt6.QtGui import QMovie, QPalette, QColor


class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

class ExpandingPushButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                background-color: lightgray;
                color: red;
            }
            QPushButton:hover {
                background-color: gray;
            }
            QPushButton:pressed {
                background-color: darkgrey;
            }
        """)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('PyQt Calculator')
        self.resize(400, 600)

        self.compute_string = ""
        label = QLabel("0")
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout = QGridLayout()

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Row 0 - full width
        layout.addWidget(label, 0, 0, 1, 12)

        def click_me_parent(symbol):
            def click_me():
                self.compute_string = self.compute_string + str(symbol)
                label.setText(self.compute_string)
                print(self.compute_string)
            return click_me

        # Rows 2-4 - 3 equal parts of 12 (each spans 4)
        for num in range(1, 10):
            btn = ExpandingPushButton(str(num))
            btn.clicked.connect(click_me_parent(num))
            layout.addWidget(btn, ((num-1)//3)+3, ((num-1)%3)*4, 1, 4)

        for num, symbol in enumerate([['+','-'],['*','/'], ['CE','=']]):
            container = QWidget()
            container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            split = QVBoxLayout(container)
            split.setContentsMargins(0, 0, 0, 0)

            btn = ExpandingPushButton(str(symbol[0]))
            split.addWidget(btn)
            btn.clicked.connect(click_me_parent(symbol[0]))

            btn = ExpandingPushButton(str(symbol[1]))
            split.addWidget(btn)
            btn.clicked.connect(click_me_parent(symbol[1]))

            layout.addWidget(container, 2, num*4, 1, 4)



if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create the main window
    window = MainWindow()
    window.show()

    # start the event loop
    sys.exit(app.exec())
