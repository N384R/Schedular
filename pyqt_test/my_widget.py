import sys
import platform

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (QDialog, QLineEdit, QVBoxLayout, QPushButton,
                             QApplication, QHBoxLayout, QLabel, QWidget, QSlider, QSizePolicy)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFontDatabase, QFont


FONT_FAMILY = ""
FONT_SIZE = 8


def set_font():
    global FONT_FAMILY
    extension = ".ttf" if platform.system() == "Windows" else ".otf"
    font_path = f"./eisenhower_legacy/fonts/Maplestory Light{extension}"
    font_id = QFontDatabase.addApplicationFont(font_path)
    FONT_FAMILY = QFontDatabase.applicationFontFamilies(font_id)[0]

    font = QFont(FONT_FAMILY, FONT_SIZE)
    QApplication.setFont(font)


class SubWidget1(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        label = QLabel("오늘의 일정", self)
        input_field = QLineEdit(self)
        layout.addWidget(label)
        layout.addWidget(input_field)


class SubWidget2(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.canvas = EisenhowerCanvas(self)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.canvas)


class EisenhowerCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure()
        super().__init__(self.fig)
        self.setParent(parent)
        self.ax = self.fig.add_subplot(111)
        self.text_labels = []
        self.font_size = FONT_SIZE
        self.set_font()
        self.draw_quadrants()

    def set_font(self):
        extension = ".ttf" if platform.system() == "Windows" else ".otf"
        font_path = f"./eisenhower/fonts/Maplestory Light{extension}"
        fm.fontManager.addfont(font_path)
        font_prop = fm.FontProperties(fname=font_path)
        plt.rcParams['font.family'] = font_prop.get_name()
        plt.rcParams['axes.unicode_minus'] = False

    def resizeEvent(self, event):
        w = self.width()
        h = self.height()
        dpi = self.fig.get_dpi()

        size = min(w, h)
        self.fig.set_size_inches(size / dpi, size / dpi, forward=True)

        self.ax.set_aspect('equal', adjustable='box')
        self.draw_idle()

        super().resizeEvent(event)

    def draw_quadrants(self):
        ax = self.ax
        ax.clear()
        self.text_labels.clear()

        ax.set_aspect('equal')

        colors = [["#f0f0ff", "#e0ffe0"], ["#fff0e0", "#ffe0e0"]]
        for i in range(2):
            for j in range(2):
                ax.axhspan(3 * j, 3 * (j + 1), xmin=0.0 + 0.5 * i,
                           xmax=0.5 + 0.5 * i, facecolor=colors[j][i], zorder=0)

        ax.set_xlim(0, 6)
        ax.set_ylim(0, 6)
        ax.set_xticks(range(1, 6))
        ax.set_yticks(range(1, 6))
        ax.set_xlabel("긴급도")
        ax.set_ylabel("중요도")
        ax.set_title("할 일", fontsize=self.font_size + 4)

        self.text_labels.append(
            ax.text(0.2, 5.75, "중요하지만 덜 긴급", fontsize=self.font_size,
                    bbox={'facecolor': 'white', 'edgecolor': 'black'}, ha='left', va='top'))
        self.text_labels.append(
            ax.text(5.8, 5.75, "긴급 & 중요", fontsize=self.font_size,
                    bbox={'facecolor': 'white', 'edgecolor': 'black'}, ha='right', va='top'))
        self.text_labels.append(
            ax.text(0.2, 0.25, "덜 중요 & 덜 긴급", fontsize=self.font_size,
                    bbox={'facecolor': 'white', 'edgecolor': 'black'}, ha='left', va='bottom'))
        self.text_labels.append(
            ax.text(5.8, 0.25, "긴급하지만 덜 중요", fontsize=self.font_size,
                    bbox={'facecolor': 'white', 'edgecolor': 'black'}, ha='right', va='bottom'))

        ax.grid(True, linestyle='--', alpha=0.7)
        self.draw()

    def adjust_font_size(self, delta: int):
        self.font_size = max(6, self.font_size + delta)
        for t in self.text_labels:
            t.set_fontsize(self.font_size)
        self.ax.set_title("할 일", fontsize=self.font_size + 4)
        self.ax.set_xlabel("긴급도", fontsize=self.font_size)
        self.ax.set_ylabel("중요도", fontsize=self.font_size)
        self.ax.tick_params(axis='both', labelsize=self.font_size)
        self.draw()


class FontResizeButton(QPushButton):
    def __init__(self, label, root_widget, mode="up", parent=None):
        super().__init__(label, parent)
        assert mode in ("up", "down"), "mode는 'up' 또는 'down'이어야 합니다."
        self.root_widget = root_widget
        self.mode = mode
        self.setFixedSize(QSize(60, 30))
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: '#f0f0f0';
                color: black;
                border: 1px solid #333333;
                font-family: '{FONT_FAMILY}';
                font-size: {FONT_SIZE + 4}px;
            }}
            QPushButton:hover {{
                background-color: '#d0f0f0';
            }}
        """)
        self.clicked.connect(self.adjust_font_size)

    def adjust_font_size(self):
        delta = 1 if self.mode == "up" else -1
        font = QApplication.font()
        size = font.pointSize()
        new_size = max(6, size + delta)
        font.setPointSize(new_size)
        QApplication.setFont(font)

        def apply_font_recursively(widget):
            widget.setFont(font)
            for child in widget.findChildren(QWidget):
                apply_font_recursively(child)

        apply_font_recursively(self.window())

        for widget in self.window().findChildren(EisenhowerCanvas):
            widget.adjust_font_size(delta)


class TitleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        title_label = QLabel("아이젠하워 시간 관리", self)
        layout.addWidget(title_label)

        self.pin_button = QPushButton("📌", self)
        self.pin_button.setCheckable(True)
        self.pin_button.setFixedSize(25, 25)
        self.pin_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                font-family: '{FONT_FAMILY}';
                font-size: {FONT_SIZE + 6}px;
                color: #666666;
            }}
            QPushButton:checked {{
                color: #0078D7;
            }}
        """)
        self.pin_button.clicked.connect(self.toggle_pin)

        close_button = QPushButton("×", self)
        close_button.setFixedSize(25, 25)
        close_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                color: #333333;
                font-family: '{FONT_FAMILY}';
                font-size: {FONT_SIZE + 10}px;
            }}
            QPushButton:hover {{
                background-color: #FF0000;
                color: white;
                border-radius: 5px;
            }}
        """)
        close_button.clicked.connect(self._parent.close)

        layout.addStretch()
        layout.addWidget(self.pin_button)
        layout.addWidget(close_button)

    def toggle_pin(self):
        flags = self._parent.windowFlags()
        stays_on_top = bool(flags & Qt.WindowStaysOnTopHint)

        if self.pin_button.isChecked() and not stays_on_top:
            self._parent.setWindowFlags(flags | Qt.WindowStaysOnTopHint)
            self._parent.show()
        elif not self.pin_button.isChecked() and stays_on_top:
            self._parent.setWindowFlags(flags & ~Qt.WindowStaysOnTopHint)
            self._parent.show()


class ButtonBox(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)

        add_task_btn = QPushButton("할 일 추가", self)
        add_task_btn.setFixedSize(QSize(60, 30))
        add_task_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: '#f0f0f0';
                border: 1px solid #333333;
                font-family: '{FONT_FAMILY}';
                font-size: {FONT_SIZE + 2}px;
            }}
            QPushButton:hover {{
                background-color: '#d0f0f0';
            }}
        """)

        font_up_btn = FontResizeButton("폰트 크기 +", parent, "up", self)
        font_down_btn = FontResizeButton("폰트 크기 -", parent, "down", self)

        reset_btn = QPushButton("Reset", self)
        reset_btn.setFixedSize(QSize(60, 30))
        reset_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: '#f0f0f0';
                border: 1px solid #333333;
                font-family: '{FONT_FAMILY}';
                font-size: {FONT_SIZE + 2}px;
            }}
            QPushButton:hover {{
                background-color: '#d0f0f0';
            }}
        """)

        layout.addStretch()
        layout.addWidget(add_task_btn)
        layout.addSpacing(20)
        layout.addWidget(font_up_btn)
        layout.addWidget(font_down_btn)
        layout.addSpacing(40)
        layout.addWidget(reset_btn)


class SliderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        label = QLabel("총 시간 (분)", self)
        label.setFixedWidth(80)
        layout.addWidget(label)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(30, 600)
        self.slider.setValue(300)
        self.slider.setTickInterval(5)
        self.slider.setFixedHeight(20)
        layout.addWidget(self.slider, stretch=1)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {{
                border: 1px solid #999999;
                height: 10px;
                background: #e0f7fa;
                margin: 0px;
                border-radius: 5px;
            }}

            QSlider::handle:horizontal {{
                background: #00bcd4;
                border: 1px solid #007a8a;
                width: 18px;
                height: 18px;
                margin: -5px 0;  /* 중심 정렬 */
                border-radius: 9px;
            }}

            QSlider::handle:horizontal:hover {{
                background: #26c6da;
                border: 1px solid #0097a7;
            }}
        """)

        self.value_display = QLineEdit(str(self.slider.value()), self)
        self.value_display.setFixedSize(60, 30)
        self.value_display.setAlignment(Qt.AlignCenter)
        self.value_display.setStyleSheet(f"""
            QLineEdit {{
                font-family: '{FONT_FAMILY}';
                font-size: {FONT_SIZE + 2}px;
                border: 1px solid #999;
            }}
        """)
        layout.addWidget(self.value_display)

        # 양방향 연결
        self.slider.valueChanged.connect(self.update_display)
        self.value_display.editingFinished.connect(self.update_slider)

    def update_display(self, value):
        self.value_display.setText(str(value))

    def update_slider(self):
        text = self.value_display.text()
        try:
            val = int(text)
            val = min(max(val, self.slider.minimum()), self.slider.maximum())
            self.slider.setValue(val)
        except ValueError:
            # 숫자 아닌 입력은 현재 슬라이더 값으로 복원
            self.value_display.setText(str(self.slider.value()))


class BodyWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.sub_widget_1 = SubWidget1(self)
        self.sub_widget_2 = SubWidget2(self)

        layout.addWidget(self.sub_widget_1)
        layout.addWidget(self.sub_widget_2)


class BottomWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        slider_widget = SliderWidget(self)
        layout.addWidget(slider_widget)

        button_box = ButtonBox(self)
        layout.addWidget(button_box)


class MainWidget(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        set_font()
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.bg_widget = QWidget(self)
        self.bg_widget.setObjectName("bgWidget")
        bg_layout = QVBoxLayout(self.bg_widget)
        bg_layout.setContentsMargins(15, 10, 15, 15)
        bg_layout.setSpacing(5)

        self.title_widget = TitleWidget(self)
        bg_layout.addWidget(self.title_widget)

        self.body_widget = BodyWidget(self)
        bg_layout.addWidget(self.body_widget)

        self.bottom_widget = BottomWidget(self)
        bg_layout.addWidget(self.bottom_widget)

        self.main_layout.addWidget(self.bg_widget)
        self.bg_widget.setStyleSheet("""
            QWidget#bgWidget {
                background-color: white;
                border: 2px solid #333333;
                border-radius: 0x;
            }
        """)

        self.old_pos = None
        self.resizing = False
        self._resize_margin = 10
        self.apply_mouse_tracking()

    def apply_mouse_tracking(self):
        self.setMouseTracking(True)
        for child in self.findChildren(QWidget):
            child.setMouseTracking(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self._is_in_resize_zone(event.pos()):
                self.resizing = True
            else:
                self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        global_pos = event.globalPos()

        if self.resizing:
            diff = global_pos - self.mapToGlobal(self.rect().bottomRight())
            new_width = max(self.minimumWidth(), self.width() + diff.x())
            new_height = max(self.minimumHeight(), self.height() + diff.y())
            self.resize(new_width, new_height)
        else:
            if self._is_in_resize_zone(event.pos()):
                self.setCursor(Qt.SizeFDiagCursor)
            else:
                self.setCursor(Qt.ArrowCursor)

            if event.buttons() & Qt.LeftButton and self.old_pos:
                delta = global_pos - self.old_pos
                self.move(self.pos() + delta)
                self.old_pos = global_pos

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.resizing = False
            self.setCursor(Qt.ArrowCursor)

    def _is_in_resize_zone(self, pos):
        return (
            self.width() - self._resize_margin <= pos.x() <= self.width()
            and self.height() - self._resize_margin <= pos.y() <= self.height()
        )

    def apply_font_recursively(self, widget):
        font = QApplication.font()
        widget.setFont(font)
        for child in widget.findChildren(QWidget):
            child.setFont(font)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    set_font()
    main_widget = MainWidget()
    main_widget.show()
    sys.exit(app.exec_())
