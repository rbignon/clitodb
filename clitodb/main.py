import builtins

from xonsh.shell import Shell

class CLItoDB(Shell):
    def cmdloop(self):
        builtins.__xonsh_shell__ = self
        builtins.__xonsh_subproc_uncaptured__ = self.sql_cmd
        builtins.__xonsh_subproc_captured_stdout__ = self.sql_cmd
        builtins.__xonsh_subproc_captured_inject__ = self.sql_cmd
        builtins.__xonsh_subproc_captured_object__ = self.sql_cmd
        builtins.__xonsh_subproc_captured_hiddenobject__ = self.sql_cmd
        builtins.__xonsh_env__['PROMPT'] = '{BOLD_CYAN}{user}{BOLD_WHITE}@{BOLD_GREEN}{hostname}{BOLD_BLUE}:budgea>{NO_COLOR} '
        self.shell.cmdloop()

    def sql_cmd(self, *args, **kwargs):
        print(args, kwargs)
