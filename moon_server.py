#!/usr/bin/env python
import os
import sys
import argparse
from moon.core.pap import get_pap
import logging
from moon.log_repository import get_log_manager
from moon.core.pdp.authz import toggle_init_flag

LOG_LEVEL = logging.INFO
LOGS = get_log_manager()

FORMAT = "%(name)s-%(levelname)s %(message)s\033[1;m"
logging.basicConfig(format=FORMAT, level=LOG_LEVEL)
logging.addLevelName(logging.INFO, "\033[1;32m%s" % logging.getLevelName(logging.INFO))
logging.addLevelName(logging.WARNING, "\033[1;31m%s" % logging.getLevelName(logging.WARNING))
logging.addLevelName(logging.ERROR, "\033[1;41m%s" % logging.getLevelName(logging.ERROR))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("djangoargs", nargs='*', help="Set Django specific arguments")
    parser.add_argument("--dbdrop", action='store_true', help="Delete local DBs")
    parser.add_argument("--keystone_sync", "--sync", action='store_true', help="Synchronize local DBs with Keystone DB")
    parser.add_argument("--run", action='store_true', help="Create local DBs and populate them")
    # parser.add_argument("--username", "-u", type=str, help="Username for Keystone remote database")
    # parser.add_argument("--userpass", "-p", type=str, help="Password for Keystone remote database")
    # parser.add_argument("--unittest", action='store_true', help="Execute tests")
    # parser.add_argument("--testonly", action='store_true', help="Check for Keystone connection and "
    #                                                             "show what it would do.")
    args = parser.parse_args()

    pap = get_pap()

    if args.dbdrop:
        pap.delete_tables()
    elif args.run:
        LOGS.write("Starting application")
        if args.keystone_sync:
            toggle_init_flag()
            pap.sync_db_with_keystone()
            toggle_init_flag()
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moon.gui.settings")
        d_args = [sys.argv[0]]
        d_args.extend(args.djangoargs)
        if "syncdb" in d_args:
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
        else:
            from django.core.management import execute_from_command_line
            execute_from_command_line(d_args)
    elif args.keystone_sync:
        toggle_init_flag()
        pap.sync_db_with_keystone()
        toggle_init_flag()
    # elif args.test:
    #     sys.argv.remove("--test")
    #     # TODO: add tests
    else:
        parser.print_usage()
