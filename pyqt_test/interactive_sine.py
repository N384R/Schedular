import sys
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore


class DraggablePoint(pg.ScatterPlotItem):
    def __init__(self, x, y, update_callback):
        super().__init__(x=[x], y=[y], symbol='o',
                         size=12, brush='r', pen=pg.mkPen(None))
        self.setZValue(10)
        self.update_callback = update_callback
        self.moving = False

    def mouseDragEvent(self, ev):
        if ev.button() != QtCore.Qt.LeftButton:
            ev.ignore()
            return

        ev.accept()  # ★ 이걸 호출해야 ViewBox 확대 방지됨

        if ev.isStart():
            self.moving = True

        elif ev.isFinish():
            self.moving = False

        elif self.moving:
            pos = ev.pos()
            x = pos.x()
            y = np.sin(x)  # y 좌표는 sin(x)로 고정
            self.setData(x=[x], y=[y])
            self.update_callback(x, y)


class SinePlot(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("드래그 가능한 Sine 곡선 위의 점")

        self.plot_widget = pg.PlotWidget()
        self.setCentralWidget(self.plot_widget)

        self.x_vals = np.linspace(0, 10, 1000)
        self.y_vals = np.sin(self.x_vals)
        self.plot_widget.plot(self.x_vals, self.y_vals, pen='b')

        self.point = DraggablePoint(2, np.sin(2), self.on_point_update)
        self.plot_widget.addItem(self.point)

        self.label = pg.TextItem(text="", anchor=(0.5, 1.5), color='k')
        self.plot_widget.addItem(self.label)
        self.on_point_update(2, np.sin(2))

    def on_point_update(self, x, y):
        self.label.setText(f"x = {x:.2f}, y = {y:.2f}")
        self.label.setPos(x, y)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = SinePlot()
    win.resize(800, 600)
    win.show()
    sys.exit(app.exec_())
