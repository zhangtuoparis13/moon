#!/usr/bin/env python
import os
import sys
import argparse
from moon_server.tools.log import get_sys_logger

sys_logger = get_sys_logger()


def start_django(args):
    from django.core.management import execute_from_command_line
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moon.settings")
    try:
        execute_from_command_line(args)
    except:
        import traceback
        print(traceback.print_exc())


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
    from moon.core.pip import get_pip
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
    parser = argparse.ArgumentParser()
    parser.add_argument("djangoargs", nargs='*', help="Set Django specific arguments")
    parser.add_argument("--dbdrop", action='store_true', help="Delete local DBs")
    parser.add_argument("--sync", help="Synchronize local DBs with 'json' or 'database'")
    parser.add_argument("--policies", help="Set a directory containing policies")
    parser.add_argument("--init", help="Initialize the django database")
    parser.add_argument("--run", action='store_true', help="Run the server")

    args = parser.parse_args()
    from moon.core.pap import get_pap
    pap = get_pap()

    find_admin_uuid()

    if args.init:
        init_django()
    if args.policies:
        pap.set_policies(args.policies)
    if args.dbdrop:
        pap.delete_tables()
    elif args.sync:
        if args.sync == "db":
            pap.add_from_db()
        else:
            for dirname in args.sync.split(","):
                pap.add_from_json(dirname.strip())
        sys_logger.info("Starting application")
        d_args = [sys.argv[0]]
        d_args.extend(args.djangoargs)
        start_django(d_args)
    elif args.run:
        sys_logger.info("Starting application")
        d_args = [sys.argv[0]]
        d_args.extend(args.djangoargs)
        start_django(d_args)
    else:
        parser.print_usage()
