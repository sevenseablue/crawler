# -*- encoding: utf-8 -*-

import logging
import date_utils
import datetime
import config

logger = None

def getlogger(busi, date1):

    # 创建一个logger
    logger = logging.getLogger(busi+date1)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        dt = date_utils.dt_date_to_str(datetime.datetime.now())
        fh = logging.FileHandler("/".join([config._data_dir, busi, date1, 'four_lines.log']) )
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter("[%(asctime)s-%(name)s(%(levelname)s)%(filename)s:%(lineno)d]%(message)s")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger





if __name__ == "__main__":
    logger = getlogger()
    logger.info("good")
    logger.info("good %s", "good")
