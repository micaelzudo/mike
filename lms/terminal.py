import cmd
import asyncio
import os
from types import MethodType, FunctionType
from collections.abc import Callable
import lms.defaults as defaults
# from lms.utils import data_dumper
# from lms.core import store

async def a_input(prompt: str = "8> ") -> str:
    return await asyncio.to_thread(input, f'{prompt}')

class terminalizer(cmd.Cmd):
    
    def __init__(self, working_dir: str = defaults.working_dir, prompt: str = "8> ",
                 intro: str = "Lulu Terminal.   Type help or ? to list commands.\n", variables: dict = {}):
        super().__init__()
        self.variables = variables
        # self.set_builtin_variables()
        self.do_chdir(working_dir)
        self.prompt = prompt
        self.intro = intro
        self.should_stop = False
        self.agent = None
        
    def add_method(self, name: str, method: Callable):
        setattr(self, name, MethodType(method, self))

    def add_method_from_code(self, name: str, method_code: str):
        compiled_function = compile(method_code, "<string>", "exec")
        registered_function = FunctionType(compiled_function.co_consts[0], globals(), name)
        setattr(self, name, MethodType(registered_function, self))

    async def a_cmdloop(self):
        print(self.intro)
        self.should_stop = False
        while not self.should_stop:
            cmd = await a_input(self.prompt)
            if cmd:
                self.should_stop = self.onecmd(cmd)
            else:
                pass #handle empty input
    
    def do_vars(self, arg):
        """Display variables currently stored internally."""
        print(self.variables)
    
    #do_mkdir

    def do_chdir(self, arg):
        """Sets the working directory."""
        try:
            os.chdir(arg)
            self.working_dir = os.getcwd()
        except Exception as e:
            print(f"Exception: {e}")
    
    def do_cd(self, arg):
        """Sets the working directory."""
        self.do_chdir(arg)
    
    def do_pwd(self, arg):
        """Shows the working directory path."""
        print(self.working_dir)
    
    def do_list(self, arg):
        """List the working directory contents."""
        try:
            print(os.listdir(self.working_dir))
        except Exception as e:
            print(f"Exception: {e}")
    
    def do_ls(self, arg):
        """List the working directory contents."""
        self.do_list(arg)
        
    def do_exit(self, arg):
        """Exits the application."""
        return True  # Stop running commands

    def default(self, arg):
        """Handles non registered commands."""
        cmd_splitted = arg.split(maxsplit=1)
        if cmd_splitted[0] in self.variables:
            if callable(self.variables[cmd_splitted[0]]):
                print(self.variables[cmd_splitted[0]](self, cmd_splitted[1] if len(cmd_splitted) > 1 else None))
            else:
                print(self.variables[cmd_splitted[0]])
        else:
            if getattr(self, "default_callback", None):
                self.default_callback(arg)
            else:
                print("Unknown command: ", cmd_splitted[0])
