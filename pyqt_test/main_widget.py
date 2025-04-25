import sys
import platform

from PyQt5.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QPushButton, QApplication, QHBoxLayout, QLabel, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase


class MainWidget(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        font_family = self.set_font()
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.bg_widget = QWidget(self)
        self.bg_widget.setObjectName("bgWidget")
        bg_layout = QVBoxLayout(self.bg_widget)
        bg_layout.setContentsMargins(15, 10, 15, 15)
        bg_layout.setSpacing(5)

        self.title_layout = QHBoxLayout()
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        self.title_layout.setSpacing(0)

        title_label = QLabel("할 일 추가", self)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: #333333;
                font-family: '{font_family}';
                font-size: 16px;
            }}
        """)
        self.title_layout.addWidget(title_label)

        close_button = QPushButton("×", self)
        close_button.setFixedSize(25, 25)
        close_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                color: #333333;
                font-family: '{font_family}';
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: #FF0000;
                color: white;
                border-radius: 5px;
            }}
        """)
        close_button.clicked.connect(self.close)
        self.title_layout.addWidget(close_button)

        bg_layout.addLayout(self.title_layout)

        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("할 일을 입력하세요")
        self.input_field.setMinimumHeight(40)
        self.input_field.setStyleSheet(f"""
            QLineEdit {{
                border: 2px solid #CCCCCC;
                border-radius: 5px;
                padding: 5px 10px;
                background-color: white;
                font-family: '{font_family}';
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border-color: #00A0A0;
            }}
        """)
        self.input_field.returnPressed.connect(self.accept)
        bg_layout.addWidget(self.input_field)

        confirm_button = QPushButton("확인", self)
        confirm_button.setMinimumHeight(40)
        confirm_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #00A0A0;
                border: none;
                border-radius: 5px;
                color: white;
                font-family: '{font_family}';
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: #008080;
            }}
        """)
        confirm_button.clicked.connect(self.accept)
        bg_layout.addWidget(confirm_button)

        self.main_layout.addWidget(self.bg_widget)

        self.bg_widget.setStyleSheet("""
            QWidget#bgWidget {
                background-color: white;
                border: 2px solid #333333;
                border-radius: 10px;
            }
        """)

        self.setFixedSize(300, 150)
        self.old_pos = None

        self.input_field.setFocus()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPos() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPos()

    def set_font(self):
        # Maplestory 폰트 설정
        extension = ".ttf" if platform.system() == "Windows" else ".otf"
        font_path = f"./eisenhower_legacy/fonts/Maplestory Light{extension}"
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QApplication.font()
        font.setFamily(font_family)
        QApplication.setFont(font)
        return font_family


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_widget = MainWidget()
    main_widget.show()
    sys.exit(app.exec_())
