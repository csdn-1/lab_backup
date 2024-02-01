from os import path
from pydm import Display
from PyQt5.QtGui import QColor
import epics
import numpy as np
import re
import threading
import subprocess


class BunchIDShow(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(BunchIDShow, self).__init__(parent=parent, args=args, macros=macros)

        self.input_bSize = self.ui.lineEdit_bSize
        self.input_IP = self.ui.lineEdit_IP
        self.update_bSize_button = self.ui.pushButton_bSize
        self.update_IP_button = self.ui.pushButton_IP
        self.run_button = self.ui.pushButton_run
        self.stop_button = self.ui.pushButton_stop
        # self.showAA_button=self.ui.pushButton_showAA
        self.status_label = self.ui.label_Status
        self.bunchid_ui_1 = self.ui.PyDMEmbeddedDisplay1

        self.update_bSize_button.clicked.connect(self.update_bSzie)
        self.update_IP_button.clicked.connect(self.update_IP)
        self.run_button.clicked.connect(self.run)
        self.stop_button.clicked.connect(self.stop)
        # self.showAA_button.clicked.connect(self.showAA)

        # self.stop_label = False
        # self.First_time_run=True
        # 添加运行状态指示灯

    def ui_filename(self):
        return "BunchIDShow.ui"

    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())

    def update_bSzie(self):
        new_bSize = self.input_bSize.text()
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

    def update_IP(self):
        return 0

    def run(self):
        # 创建两个线程来执行两个命令
        thread1 = threading.Thread(target=self.runIOC)
        self.bunchid_ui_1.connect()
        # thread2 = threading.Thread(target=self.runUI)
        self.stop_label = False

        # 启动这两个线程
        thread1.start()
        # thread2.start()

    def runIOC(self):
        try:
            cmd1 = "./lzy_udp_server.cmd"
            # subprocess.run(
            process1 = subprocess.Popen(
                cmd1,
                cwd="/home/zmq/epics/BunchId_server_udp/iocBoot/iocbunchid_server",
                shell=True,
                text=True,
                # check=True,
            )
            self.status_label.setText("Status: Command 1 executed successfully.")
            while True:
                if self.stop_label:
                    process1.terminate()  # 终止 cmd1 的执行
                    break

        # except subprocess.CalledProcessError as e:
        #     self.status_label.setText("Status: Command 1 execution failed.")
        #     print("Command 1 execution failed:", e)
        except Exception as e:
            self.status_label.setText("Status: An error occurred.")
            print("An error occurred:", e)

    def runUI(self):
        try:
            cmd2 = 'pydm -m \'{"P":"myIPServer"}\' FrameNum_and_BunchIDNum_plot.ui'
            # subprocess.run(
            process1 = subprocess.Popen(
                cmd2,
                cwd="/home/zmq/lzy/BunchID_UI",
                shell=True,
                text=True,
                # check=True
            )
            while True:
                if self.stop_label:
                    process1.terminate()  # 终止 cmd1 的执行
                    break
            self.status_label.setText("Status: Command 2 executed successfully.")
        # except subprocess.CalledProcessError as e:
        #     self.status_label.setText("Status: Command 2 execution failed.")
        #     print("Command 2 execution failed:", e)
        except Exception as e:
            self.status_label.setText("Status: An error occurred.")
            print("An error occurred:", e)

    def stop(self):
        self.bunchid_ui_1.disconnect()
        self.stop_label = True

    # def waveShow(self):
    #     # 设置背景颜色
    #     self.wavePlot.setBackground("w")
    #     wav_y = np.array(epics.caget("myIPServer:BunchID"))
    #     self.FrameNum = self.wavePlot.addYChannel(
    #         # y_channel="ca://myIPServer:FrameNum",
    #         # y_channel="ca://myIPServer:BunchID",
    #         y_channel=wav_y,
    #         name="myIPServer:FrameNum",
    #         color=QColor("red"),
    #         lineStyle=1,  # 离大谱    https://doc.qt.io/qt-5/qt.html#PenStyle-enum
    #         lineWidth=1,
    #         # symbol="None",
    #         # symbolSize=10,
    #         # yAxisName="Axis1",
    #     )
    # def update_bSize(self):
