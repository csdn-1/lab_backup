import sys
import subprocess
import threading
import re
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Update bSize and Run Commands")
        self.setGeometry(100, 100, 600, 300)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        label = QLabel("Enter an integer for bSize:")
        self.input_box = QLineEdit()
        self.update_button = QPushButton("Update bSize")
        self.run_button = QPushButton("Run Commands")
        self.status_label = QLabel("Status: ")

        self.update_button.clicked.connect(self.update_bSize)
        self.run_button.clicked.connect(self.runCommands)

        layout.addWidget(label)
        layout.addWidget(self.input_box)
        layout.addWidget(self.update_button)
        layout.addWidget(self.run_button)
        layout.addWidget(self.status_label)

        central_widget.setLayout(layout)

    def update_bSize(self):
        # 获取用户输入的整数
        new_bSize = self.input_box.text()

        try:
            # 打开文件并读取内容
            with open(
                "/home/zmq/epics/BunchId_server_udp/iocBoot/iocbunchid_server/lzy_udp_server.cmd",
                "r",
            ) as file:
                file_content = file.read()

            # 使用正则表达式替换 "bSize=" 后的数字
            updated_content = re.sub(r"bSize=\d+", f"bSize={new_bSize}", file_content)

            # 将更新后的内容写回文件
            with open(
                "/home/zmq/epics/BunchId_server_udp/iocBoot/iocbunchid_server/lzy_udp_server.cmd",
                "w",
            ) as file:
                file.write(updated_content)

            self.status_label.setText("Status: Updated successfully.")

        except Exception as e:
            self.status_label.setText("Status: Update failed.")
            print("An error occurred:", e)

    def runCommands(self):
        # 创建两个线程来执行两个命令
        thread1 = threading.Thread(target=self.execute_command_1)
        thread2 = threading.Thread(target=self.execute_command_2)

        # 启动这两个线程
        thread1.start()
        thread2.start()

    def execute_command_1(self):
        try:
            cmd1 = "./lzy_udp_server.cmd"
            subprocess.run(
                cmd1,
                cwd="/home/zmq/epics/BunchId_server_udp/iocBoot/iocbunchid_server",
                shell=True,
                text=True,
                check=True,
            )
            self.status_label.setText("Status: Command 1 executed successfully.")
        except subprocess.CalledProcessError as e:
            self.status_label.setText("Status: Command 1 execution failed.")
            print("Command 1 execution failed:", e)
        except Exception as e:
            self.status_label.setText("Status: An error occurred.")
            print("An error occurred:", e)

    def execute_command_2(self):
        try:
            cmd2 = 'pydm -m \'{"P":"myIPServer"}\' test.ui'
            subprocess.run(
                cmd2, cwd="/home/zmq/lzy/BunchID_UI", shell=True, text=True, check=True
            )
            self.status_label.setText("Status: Command 2 executed successfully.")
        except subprocess.CalledProcessError as e:
            self.status_label.setText("Status: Command 2 execution failed.")
            print("Command 2 execution failed:", e)
        except Exception as e:
            self.status_label.setText("Status: An error occurred.")
            print("An error occurred:", e)


def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
