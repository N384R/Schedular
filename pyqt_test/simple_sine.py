import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
)
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas
)
from matplotlib.figure import Figure


class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.ax = self.canvas.figure.add_subplot(111)

        self.button = QPushButton("그래프 업데이트")
        self.button.clicked.connect(self.plot_graph)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.plot_graph()

    def plot_graph(self):
        self.ax.clear()
        x = np.linspace(0, 10, 100)
        y = np.sin(x + np.random.uniform(0, 2*np.pi))  # 무작위 위상 변화
        self.ax.plot(x, y)
        self.ax.set_title("Sine Wave with Random Phase")
        self.canvas.draw()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 + Matplotlib 그래프 예제")
        self.setCentralWidget(MatplotlibWidget(self))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
