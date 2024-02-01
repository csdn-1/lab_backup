import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from pydm.widgets import PyDMWaveformPlot
from pydm import Display


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("PyQt and PyDM Waveform Plot")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # 创建PyDM Waveform Plot小部件
        self.plot_widget = PyDMWaveformPlot()
        self.plot_widget.setMinimumSize(400, 300)

        layout.addWidget(self.plot_widget)

        central_widget.setLayout(layout)

        # 在Waveform Plot小部件中添加一条曲线
        self.plot_widget.add_curve("Sine Wave", color="blue")


def main():
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
