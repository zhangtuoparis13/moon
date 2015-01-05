# Copyright 2014 Orange
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

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

urllib3_logger = logging.getLogger('urllib3')
urllib3_logger.setLevel(logging.CRITICAL)

def get_sys_logger():
    return sys_logger


def get_authz_logger():
    return authz_logger

