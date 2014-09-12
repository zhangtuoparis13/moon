import logging


authz_logger = logging.getLogger('authz')
authz_logger.setLevel(logging.WARNING)
fh = logging.FileHandler('/var/log/moon/authz.log')
fh.setLevel(logging.WARNING)
authz_logger.addHandler(fh)



# authz_logger.warning('yyyy')

