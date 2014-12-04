import logging

LOG_LEVEL = logging.INFO

authz_logger = logging.getLogger('authz')
authz_logger.setLevel(logging.WARNING)
fh = logging.FileHandler('/var/log/moon/authz.log')
fh.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s ------ %(message)s')
fh.setFormatter(formatter)
authz_logger.addHandler(fh)

FORMAT = "%(name)s-%(levelname)s %(message)s\033[1;m"
logging.basicConfig(format=FORMAT, level=LOG_LEVEL)
logging.addLevelName(logging.INFO, "\033[1;32m%s" % logging.getLevelName(logging.INFO))
logging.addLevelName(logging.WARNING, "\033[1;31m%s" % logging.getLevelName(logging.WARNING))
logging.addLevelName(logging.ERROR, "\033[1;41m%s" % logging.getLevelName(logging.ERROR))

sys_logger = logging.getLogger('sys')
sys_logger.setLevel(logging.WARNING)
fh = logging.FileHandler('/var/log/moon/sys.log')
fh.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s ------ %(message)s')
fh.setFormatter(formatter)
sys_logger.addHandler(fh)


def get_sys_logger():
    return sys_logger


def get_authz_logger():
    return authz_logger

