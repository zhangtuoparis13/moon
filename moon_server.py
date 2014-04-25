#!/usr/bin/env python
import os
import sys
import argparse
# from core.pap.core import PAP
from moon.core.pip.sync_db import create_tables, populate_dbs
import logging

LOG_LEVEL = logging.INFO

FORMAT = "%(name)s-%(levelname)s %(message)s\033[1;m"
logging.basicConfig(format=FORMAT, level=LOG_LEVEL)
logging.addLevelName(logging.INFO, "\033[1;32m%s" % logging.getLevelName(logging.INFO))
logging.addLevelName(logging.WARNING, "\033[1;31m%s" % logging.getLevelName(logging.WARNING))
logging.addLevelName(logging.ERROR, "\033[1;41m%s" % logging.getLevelName(logging.ERROR))

# from moon.info_repository import driver_dispatcher as dd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("djangoargs", nargs='*', help="Set Django specific arguments")
    parser.add_argument("--dbcreate", action='store_true', help="Create local DBs and populate them")
    parser.add_argument("--run", action='store_true', help="Create local DBs and populate them")
    parser.add_argument("--username", "-u", type=str, help="Username for Keystone remote database")
    parser.add_argument("--userpass", "-p", type=str, help="Password for Keystone remote database")
    parser.add_argument("--unittest", action='store_true', help="Execute tests")
    args = parser.parse_args()

    if args.dbcreate:
        create_tables()
        if args.userpass:
            populate_dbs(username=args.username, password=args.userpass)
        elif args.username:
            populate_dbs(username=args.username)
        else:
            populate_dbs()
    elif args.run:
        # Re-create table because the server is starting
        create_tables()
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gi.settings")
        from django.core.management import execute_from_command_line
        d_args = [sys.argv[0]]
        d_args.extend(args.djangoargs)
        execute_from_command_line(d_args)
    elif args.test:
        sys.argv.remove("--test")
        # TODO: add tests
    else:
        parser.print_usage()
        pass
