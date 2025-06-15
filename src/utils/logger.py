import logging


def get_logger(name):
    logger = logging.getLogger(name)

    # 如果logger已经有处理器，说明已经被配置过，直接返回
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # 创建控制台处理器
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # 优化美观的格式化器
    formatter = logging.Formatter(
        '\033[1m%(asctime)s | %(levelname)-8s | %(name)s\033[0m\n  => %(message)s',
        datefmt='%Y-%m-%d %H:%M'  # 保留年月日和时分
    )
    ch.setFormatter(formatter)

    # 将处理器添加到日志记录器
    logger.addHandler(ch)

    # 添加过滤器使INFO级别没有前缀
    class InfoFilter(logging.Filter):
        def filter(self, record):
            return record.levelno == logging.INFO

    # 创建更简洁的INFO级别格式化器
    info_formatter = logging.Formatter('%(asctime)s | %(message)s', datefmt='%H:%M')
    info_handler = logging.StreamHandler()
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(info_formatter)
    info_handler.addFilter(InfoFilter())
    logger.addHandler(info_handler)

    # 设置默认级别处理
    logger.propagate = False

    return logger


logger = get_logger(__name__)
