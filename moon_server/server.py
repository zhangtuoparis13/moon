#!/usr/bin/env python

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

import os
import sys
import argparse
import logging
from moon_server import config
from moon_server.tools.log.core import get_sys_logger


sys_logger = get_sys_logger()
# TODO: LOG_SYS = logging.getLogger('moon.sys')


def start_django(args):
    from django.core.management import execute_from_command_line
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moon_server.settings")
    execute_from_command_line(args)


def init_django():
    from django.contrib.auth.management.commands import changepassword
    from django.db.utils import IntegrityError
    from django.core.management import call_command
    try:
        call_command('createsuperuser', interactive=False, username="superuser", email="xx@xx.net")
        command = changepassword.Command()
        command._get_pass = lambda *args: 'password'
        command.execute("superuser")
    except IntegrityError:
        pass
    call_command(" ".join(d_args[1:]), interactive=False)


def find_admin_uuid():
    pap = get_pap()
    from moon_server.core.pip import get_pip
    pip = get_pip()
    kusers = pip.get_subjects()
    admin_user = None
    for user in kusers:
        if user["name"] == "admin":
            admin_user = user
            break
    if not admin_user:
        sys_logger.warning("Cannot find admin user in Keystone.")
        return
    pap.set_admin_uuid(admin_user["uuid"])


if __name__ == "__main__":
    CONF = config.CONF
    config.configure()
    # CONF(default_config_files=['/../../moon.conf']) : # for reflection of options

    pid = os.getpid()
    try:
        open("/var/run/moon.pid", "w").write(str(pid))
    except IOError:
        open("/tmp/moon.pid", "w").write(str(pid))

    # TODO: put the following arguments to the conf file
    parser = argparse.ArgumentParser()
    parser.add_argument("djangoargs", nargs='*', help="Set Django specific arguments")
    parser.add_argument("--policies", help="Set a directory containing policies")
    parser.add_argument("--init", help="Initialize the django database")
    parser.add_argument("--run", action='store_true', help="Run the server")

    args = parser.parse_args()
    from moon_server.core.pap import get_pap
    pap = get_pap()

    find_admin_uuid()

    if args.init:
        init_django()
    if args.policies:
        pap.set_policies(args.policies)
    if args.run:
        sys_logger.info("Starting application")
        d_args = [sys.argv[0]]
        d_args.extend(args.djangoargs)
        start_django(d_args)
    else:
        parser.print_usage()
