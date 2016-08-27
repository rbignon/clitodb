# Copyright (c) 2016 Romain Bignon
#               All Rights Reserved
#
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.


from __future__ import print_function

import builtins
import argparse
import sys
from prettytable import PrettyTable

from sqlalchemy.engine.url import URL
from sqlalchemy.exc import DatabaseError, NoSuchModuleError, ArgumentError

from xonsh.shell import Shell
from xonsh.aliases import xonsh_exit

from clitodb import __version__
from .database import Database


class CLItoDB(Shell):
    def build_parser(self):
        p = argparse.ArgumentParser(description='clitodb', add_help=False)
        p.add_argument('--help',
                       dest='help',
                       action='store_true',
                       default=False,
                       help='show help and exit')
        p.add_argument('--version',
                       dest='version',
                       action='store_true',
                       default=False,
                       help='show version information and exit')
        p.add_argument('--driver',
                       help='What driver to use to connect to database',
                       dest='driver',
                       required=False,
                       default='mysql')
        p.add_argument('-h', '--host',
                       help="Connect to the server on the given host",
                       dest='host_name',
                       required=False,
                       default='localhost')
        p.add_argument('-P', '--port',
                       help='Connect to the server on the given port',
                       dest='port_num',
                       required=False,
                       default=None)
        p.add_argument('-u', '--user',
                       help='The user name to use when connecting to the server',
                       dest='user',
                       required=False,
                       default=None)
        p.add_argument('-p', '--password',
                       help='The password to use when connecting to the server',
                       dest='password',
                       required=False,
                       default=None)
        p.add_argument('database',
                       help='Database name',
                       nargs='?',
                       default=None)
        return p

    def cmdloop(self, argv=None):
        if argv is None:
            argv = sys.argv[1:]

        parser = self.build_parser()

        args = parser.parse_args(argv)
        if args.help:
            parser.print_help()
            parser.exit()
        if args.version:
            version = '/'.join(('clitodb', __version__))
            print(version)
            parser.exit()

        try:
            self.db = Database(self.build_url(args))
        except DatabaseError as e:
            print('Unable to connect to database:', e.orig.args[-1], file=sys.stderr)
            sys.exit(1)
        except (NoSuchModuleError,ArgumentError) as e:
            print('Unable to load driver %s: %s' % (args.driver, e), file=sys.stderr)
            sys.exit(1)

        builtins.__xonsh_shell__ = self
        builtins.__xonsh_subproc_uncaptured__ = self.sql_cmd
        builtins.__xonsh_subproc_captured_stdout__ = self.sql_cmd
        builtins.__xonsh_subproc_captured_inject__ = self.sql_cmd
        builtins.__xonsh_subproc_captured_object__ = self.sql_cmd
        builtins.__xonsh_subproc_captured_hiddenobject__ = self.sql_cmd
        builtins.__xonsh_pathsearch__ = self.pathsearch
        builtins.__xonsh_globsearch__ = self.globsearch
        builtins.__xonsh_regexsearch__ = self.regexsearch
        builtins.__xonsh_glob__ = self.globpath
        builtins.__xonsh_expand_path__ = self.expand_path

        builtins.__xonsh_env__['FORMATTER_DICT']['database'] = args.database
        builtins.__xonsh_env__['FORMATTER_DICT']['user'] = args.user
        builtins.__xonsh_env__['FORMATTER_DICT']['hostname'] = args.host_name
        builtins.__xonsh_env__['PROMPT'] = '{BOLD_CYAN}{user}{BOLD_WHITE}@{BOLD_GREEN}{hostname}{BOLD_BLUE}:{database}>{NO_COLOR} '
        self.shell.cmdloop()

    def sql_cmd(self, *cmds):
        session = self.db.Session()
        try:
            for cmd in cmds:
                if cmd == ['EOF']:
                    xonsh_exit([])
                    return
                table = PrettyTable()
                try:
                    for line in session.execute(' '.join(cmd)):
                        table.add_row(line)
                except DatabaseError as e:
                    print(e)
                else:
                    print(table.get_string())
        finally:
            self.db.Session.remove()

    def build_url(self, args):
        url = URL(args.driver,
                  username=args.user,
                  password=args.password,
                  host=args.host_name,
                  port=args.port_num,
                  database=args.database,
                  query={"charset": "utf8"})

        return url

    def pathsearch(self, *args, **kwargs):
        print('pathsearch', args, kwargs)

    def globsearch(self, *args, **kwargs):
        print('globsearch', args, kwargs)

    def regexsearch(self, *args, **kwargs):
        print('regexsearch', args, kwargs)

    def globpath(self, s, ignore_case=False, return_empty=False, sort_result=None):
        return [s]

    def expand_path(self, s):
        return s
