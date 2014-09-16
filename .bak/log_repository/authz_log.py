import logging


authz_logger = logging.getLogger('authz')
authz_logger.setLevel(logging.WARNING)
fh = logging.FileHandler('/var/log/moon/authz.log')
fh.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s ------ %(message)s')
fh.setFormatter(formatter)
authz_logger.addHandler(fh)



# authz_logger.warning('yyyy')

