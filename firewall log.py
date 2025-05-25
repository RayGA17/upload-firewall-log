import time
import sys
import os


class LogTailer:
    def __init__(self, file_path, lines_to_keep):
        self.file_path = file_path
        self.lines_to_keep = lines_to_keep
        self.file_size = 0
        self.seen_lines = set()

    def check_for_new_lines(self):
        # 检查文件是否有新内容
        current_size = os.path.getsize(self.file_path)
        if current_size < self.file_size:  # 文件可能被截断或重写
            self.file_size = 0
            self.seen_lines.clear()

        with open(self.file_path, 'r') as f:
            f.seek(self.file_size)
            new_lines = f.readlines()
            # 这里更新文件指针的位置
            self.file_size = f.tell()

        # 只显示未重复的内容
        for line in new_lines:
            if line not in self.seen_lines:
                sys.stdout.write(line)
                self.seen_lines.add(line)
        sys.stdout.flush()

    def trim_log_file(self):
        with open(self.file_path, 'r') as f:
            lines = f.readlines()

        with open(self.file_path, 'w') as f:
            f.writelines(lines[-self.lines_to_keep:])


if __name__ == "__main__":
    log_file = r"C:\Windows\System32\LogFiles\Firewall\pfirewall.log"
    lines_to_keep = 100000  # 保留
    check_interval = 0.1  # 检查
    tailer = LogTailer(log_file, lines_to_keep)

    while True:
        # 显示新内容
        tailer.check_for_new_lines()
        # 修剪日志文件
        if time.time() % 60 < 0.1:
            tailer.trim_log_file()
        time.sleep(check_interval)