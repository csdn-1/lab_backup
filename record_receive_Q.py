import subprocess
import matplotlib.pyplot as plt
from datetime import datetime
import time


def get_receive_q(port):
    try:
        output = subprocess.check_output(f"ss -an | grep {port}", shell=True)
        lines = output.decode("utf-8").split("\n")
        for line in lines:
            if f":{port}" in line:
                parts = line.split()
                if len(parts) >= 6:
                    return int(parts[2]) / (1024 * 1024)  # 将字节转换为 MB
    except Exception as e:
        print("Error while running ss command:", e)
    return 0


def main():
    port_to_monitor = 2000
    time_points = []
    receive_q_values = []

    plt.ion()  # 开启交互式绘图

    fig, ax = plt.subplots()
    ax.set_xlabel("Time")
    ax.set_ylabel("Receive Queue (receive q) / MB")  # 更新纵坐标标签

    while True:
        receive_q = get_receive_q(port_to_monitor)
        timestamp = datetime.now().strftime("%H:%M:%S")

        time_points.append(timestamp)
        receive_q_values.append(receive_q)

        ax.clear()
        ax.plot(time_points, receive_q_values)
        ax.set_xlabel("Time")
        ax.set_ylabel("Receive Queue (receive q) / MB")  # 更新纵坐标标签
        ax.set_title(f"Port {port_to_monitor} Receive Queue over Time")

        
        ax.xaxis.set_major_locator(
            plt.FixedLocator(range(0, len(time_points), 3600))
        )  
        ax.xaxis.set_major_formatter(plt.FixedFormatter(time_points[::3600]))

        plt.xticks(rotation=45)
        plt.pause(1)  # 暂停1秒以便实时更新图表


if __name__ == "__main__":
    main()
