import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore


class DraggablePoint(pg.ScatterPlotItem):
    def __init__(self, x, y, color, label, callback):
        super().__init__(x=[x], y=[y], size=30,
                         brush=pg.mkBrush(color),
                         pen=None,
                         symbol='o')
        self.label = label
        self.callback = callback
        self.moving = False
        self.sigClicked.connect(self.on_click)

    def on_click(self, plot, points):
        self.moving = True

    def mouseDragEvent(self, ev):
        if ev.button() != QtCore.Qt.LeftButton:
            ev.ignore()
            return
        ev.accept()
        if ev.isStart():
            self.moving = True
        elif ev.isFinish():
            self.moving = False
        elif self.moving:
            pos = ev.pos()
            self.setData(x=[pos.x()], y=[pos.y()])
            self.callback(self.label, pos.x(), pos.y())


class CloseButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__('×', parent)
        self.setFixedSize(30, 30)
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: black;
                font-size: 18px;
                border: none;
            }
        """)
        self.setCursor(QtCore.Qt.PointingHandCursor)

    def enterEvent(self, event):
        self.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                font-size: 18px;
                border: none;
            }
        """)

    def leaveEvent(self, event):
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: black;
                font-size: 18px;
                border: none;
            }
        """)


class QuadrantPlot(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Eisenhower Matrix with Draggable Tasks")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 창 테두리 제거

        self.plot_widget = pg.PlotWidget()
        self.setCentralWidget(self.plot_widget)

        self.plot_widget.setMouseEnabled(x=False, y=False)
        self.plot_widget.setXRange(0, 6)
        self.plot_widget.setYRange(0, 6)
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.plot_widget.setBackground('w')

        # 사분면 배경 사각형 추가
        self._add_quadrant_background()

        # 드래그 가능한 점 3개 생성
        self.points = []
        self.add_task_point(2, 5, 'lightgreen', 'Operator algebra')
        self.add_task_point(2, 3, 'lightblue', 'dissipation ansatz')
        self.add_task_point(4, 4.5, 'lightcoral', 'QCQD 연구 정리')

        # 닫기 버튼 추가
        self.close_button = CloseButton(self)
        self.close_button.clicked.connect(self.close)
        self.close_button.raise_()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.close_button.move(self.width() - 40, 10)  # 우상단 위치 고정

    def _add_quadrant_background(self):
        vb = self.plot_widget.getViewBox()
        vb.addItem(self._make_rect(0, 3, 3, 3, '#fdf0d5'))  # 중요하지만 덜 긴급
        vb.addItem(self._make_rect(3, 3, 3, 3, '#f8d7da'))  # 긴급 & 중요
        vb.addItem(self._make_rect(0, 0, 3, 3, '#dbeafe'))  # 덜 중요 & 덜 긴급
        vb.addItem(self._make_rect(3, 0, 3, 3, '#d1fae5'))  # 긴급하지만 덜 중요

    def _make_rect(self, x, y, w, h, color):
        rect = QtWidgets.QGraphicsRectItem(x, y, w, h)
        rect.setBrush(pg.mkBrush(color))
        rect.setPen(pg.mkPen(None))
        return rect

    def add_task_point(self, x, y, color, label):
        point = DraggablePoint(x, y, color, label, self.on_drag)
        self.plot_widget.addItem(point)
        self.points.append(point)

    def on_drag(self, label, x, y):
        print(f"{label} → x: {x:.2f}, y: {y:.2f}")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = QuadrantPlot()
    win.resize(600, 600)
    win.show()
    sys.exit(app.exec_())
