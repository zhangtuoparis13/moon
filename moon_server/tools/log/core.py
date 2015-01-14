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


class ColorFormatter(logging.Formatter):
    def format(self, record):
        format_orig = self._fmt
        # Replace the original format with one customized by logging level
        if record.levelno == logging.WARNING:
            self._fmt = "\033[1;31m"+self._fmt+"\033[m"
        elif record.levelno == logging.INFO:
            self._fmt = "\033[1;32m"+self._fmt+"\033[m"
        elif record.levelno == logging.ERROR:
            self._fmt = "\033[1;41m"+self._fmt+"\033[m"
        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)
        # Restore the original format configured by the user
        self._fmt = format_orig
        return result

LOG_LEVEL = logging.INFO

logger_root = logging.getLogger("moon")
# Output configuration
formatter_color = ColorFormatter("%(name)s :: %(levelname)s :: %(message)s")
formatter_bw = logging.Formatter("%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s")

# Logger for authz messages
authz_logger = logging.getLogger('moon.authz')
authz_logger.setLevel(LOG_LEVEL)
authz_fh = logging.FileHandler('/var/log/moon/authz.log')
authz_fh.setLevel(LOG_LEVEL)
authz_fh.setFormatter(formatter_bw)
authz_logger.addHandler(authz_fh)
authz_st = logging.StreamHandler()
authz_st.setFormatter(formatter_color)
authz_logger.addHandler(authz_st)

# Logger for messages from the framework
sys_logger = logging.getLogger('moon.sys')
sys_logger.setLevel(LOG_LEVEL)
sys_fh = logging.FileHandler('/var/log/moon/system.log')
sys_fh.setLevel(LOG_LEVEL)
sys_fh.setFormatter(formatter_bw)
sys_logger.addHandler(sys_fh)
sys_st = logging.StreamHandler()
sys_st.setFormatter(formatter_color)
sys_logger.addHandler(sys_st)

# Delete unneeded logs from URLLIB
urllib3_logger = logging.getLogger('urllib3')
urllib3_logger.setLevel(logging.ERROR)


# Export authz and sys logger


def get_sys_logger():
    return sys_logger


def get_authz_logger():
    return authz_logger


# Decorator creation for Django views


def log_request(function):
    """Decorator for logging request in sys_logger

    :param function:
    :return:
    """
    def wrapped(*args, **kwargs):
        sys_logger.info("{} {}".format(args[0].META.get("REQUEST_METHOD"), args[0].path))
        result = function(*args, **kwargs)
        return result
    return wrapped

