import os

def find_field_in_files(folder, target_field):
    # 递归遍历文件夹及其子文件夹中的所有文件
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if target_field in content:
                        print(f"Field '{target_field}' found in file: {file_path}")
            except (IOError, OSError):
                print(f"Error reading file: {file_path}")

if __name__ == "__main__":
    target_folder = "/home/zmq/epics/modules/synApps/support/asyn-R4-42"  # 替换为要搜索的文件夹路径
    target_field = "connectionListener"      # 替换为要查找的字段

    find_field_in_files(target_folder, target_field)
