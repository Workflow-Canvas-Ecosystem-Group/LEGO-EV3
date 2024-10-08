import logging
from logging.handlers import RotatingFileHandler
import os


def setup_log(level):
    log_dir = "/home/robot/log/"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 日志文件路径
    log_file = os.path.join(log_dir, "app.log")
    logging.basicConfig(
        level=level,
        format="[%(asctime)s %(filename)s %(lineno)d] %(message)s",
        handlers=[
            RotatingFileHandler(
                log_file, maxBytes=1024 * 1024 * 5, backupCount=5  # 5MB * 5
            )
        ]
    )
    # console_basic_format = "[%(asctime)s %(filename)s %(lineno)d] %(message)s"
    # logging.basicConfig(level=level, stream=sys.stdout, format=console_basic_format)
