#!/usr/bin/env python
import os
import sys
import argparse
from moon.core.pap import get_pap
import logging
from moon.log_repository import get_log_manager

LOG_LEVEL = logging.INFO
LOGS = get_log_manager()

FORMAT = "%(name)s-%(levelname)s %(message)s\033[1;m"
logging.basicConfig(format=FORMAT, level=LOG_LEVEL)
logging.addLevelName(logging.INFO, "\033[1;32m%s" % logging.getLevelName(logging.INFO))
logging.addLevelName(logging.WARNING, "\033[1;31m%s" % logging.getLevelName(logging.WARNING))
logging.addLevelName(logging.ERROR, "\033[1;41m%s" % logging.getLevelName(logging.ERROR))


def start_django(args):
    from django.core.management import execute_from_command_line
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moon.gui.settings")
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("djangoargs", nargs='*', help="Set Django specific arguments")
    parser.add_argument("--dbdrop", action='store_true', help="Delete local DBs")
    parser.add_argument("--sync", help="Synchronize local DBs with 'json' or 'database'")
    parser.add_argument("--init", help="Initialize the django database")
    parser.add_argument("--run", action='store_true', help="Run the server")

    args = parser.parse_args()

    pap = get_pap()

    if args.init:
        init_django()
    if args.dbdrop:
        pap.delete_tables()
    elif args.sync:
        if args.sync == "db":
            pap.add_from_db()
        else:
            pap.add_from_json(args.sync)
        d_args = [sys.argv[0]]
        d_args.extend(args.djangoargs)
        start_django(d_args)
    elif args.run:
        LOGS.write("Starting application")
        d_args = [sys.argv[0]]
        d_args.extend(args.djangoargs)
        start_django(d_args)
    else:
        parser.print_usage()
