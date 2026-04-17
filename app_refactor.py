import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QGridLayout, QMainWindow, QPushButton, QSizePolicy,
)
from PyQt6.QtCore import Qt

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
            QPushButton:hover { background-color: gray; }
            QPushButton:pressed { background-color: darkgrey; }
        """)

class ExpandingQLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

# Button grid layout: (label, row, col, rowspan, colspan)
BUTTON_LAYOUT = [
    ("1", 3, 0, 1), ("2", 3, 4), ("3", 3, 8),
    ("4", 4, 0), ("5", 4, 4), ("6", 4, 8),
    ("7", 5, 0), ("8", 5, 4), ("9", 5, 8),
    ("0", 7, 0), (".", 7, 4), ("Res", 7, 8),
    (("+", 2, 0), ("-", 2, 0)),
    (("*", 2, 4), ("/", 2, 4)),
    (("=", 2, 8), ("CE", 2, 8)),
]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.expr_to_compute = ""
        self.last_result = ""
        self._build_ui()

    def _build_ui(self):
        self.setWindowTitle('PyQt Calculator')
        self.resize(400, 600)

        main_layout = QGridLayout()
        main_container = QWidget()
        main_container.setLayout(main_layout)
        self.setCentralWidget(main_container)

        self.screen = ExpandingQLabel("0")
        main_layout.addWidget(self.screen, 0, 0, 1, 12)

        self._build_buttons(main_layout)

    def _build_buttons(self, layout: QGridLayout):
        # Digits 1 to 9
        for button in BUTTON_LAYOUT[:11]:
            btn = ExpandingPushButton(button[0])
            btn.clicked.connect(lambda _, n=button[0]: self._append(n) )
            layout.addWidget(btn, button[1], button[2], 1, 4)
        # Res
        button = BUTTON_LAYOUT[11]
        btn = ExpandingPushButton(button[0])
        btn.clicked.connect(self._use_last_result)
        layout.addWidget(btn, button[1], button[2], 1, 4)
        # Top Split Row With Operations (+,-,*,/)
        for buttons in BUTTON_LAYOUT[12:14]:
            container = QWidget()
            split = QVBoxLayout(container)
            split.setContentsMargins(0,0,0,0)
            btn1 = ExpandingPushButton(buttons[0][0])
            btn1.clicked.connect(lambda _, n=buttons[0][0]: self._append(n))
            split.addWidget(btn1)
            btn2 = ExpandingPushButton(buttons[1][0])
            btn2.clicked.connect(lambda _, n=buttons[1][0]: self._append(n))
            split.addWidget(btn2)
            layout.addWidget(container, buttons[0][1], buttons[0][2], 1, 4)
        # = and CE button
        buttons = BUTTON_LAYOUT[14]
        container = QWidget()
        split = QVBoxLayout(container)
        split.setContentsMargins(0,0,0,0)
        btn1 = ExpandingPushButton(buttons[0][0])
        btn1.clicked.connect(self._eval)
        split.addWidget(btn1)
        btn2 = ExpandingPushButton(buttons[1][0])
        btn2.clicked.connect(self._reset_compute_expr)
        split.addWidget(btn2)
        layout.addWidget(container, buttons[0][1], buttons[0][2], 1, 4)

    def _append(self, symbol: str):
        self.expr_to_compute += symbol
        self.screen.setText(self.expr_to_compute)

    def _reset_compute_expr(self):
        self.expr_to_compute = ""
        self.screen.setText(self.expr_to_compute)

    def _use_last_result(self):
        self._append(self.last_result)

    def _eval(self):
        try:
            self.last_result = str(eval(self.expr_to_compute))
            self.expr_to_compute = self.last_result
            self.screen.setText(self.expr_to_compute)
        except:
            self.screen.setText("Error!")
            self.expr_to_compute = ""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
