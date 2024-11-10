import cmd
import asyncio
import os
from types import MethodType, FunctionType
from collections.abc import Callable
# from lms.utils import data_dumper
# from lms.core import store

async def a_input(prompt: str = "8> ") -> str:
    return await asyncio.to_thread(input, f'{prompt}')

class terminalizer(cmd.Cmd):
    
    def __init__(self, working_dir: str = "./working", prompt: str = "8> ",
                 intro: str = "Lulu Terminal.   Type help or ? to list commands.\n", variables: dict = {}):
        super().__init__()
        self.variables = variables
        # self.set_builtin_variables()
        self.working_dir = working_dir
        self.prompt = prompt
        self.intro = intro
        self.should_stop = False
    
    # def set_builtin_variables(self):
    #     self.variables["exit"] = None
        
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
            self.should_stop = self.onecmd(await a_input(self.prompt))
    
    # Define some callback functions for specific commands
    def do_vars(self, arg):
        """Display variables currently stored internally."""
        print(self.variables)
    
    # Define some callback functions for specific commands
    def do_chdir(self, arg):
        """Sets the working directory."""
        # TO:DO check if te path is valid
        self.working_dir = arg
    
    # Define some callback functions for specific commands
    def do_dir(self, arg):
        """Shows the working directory path."""
        print(self.working_dir)
    
    # Define some callback functions for specific commands
    def do_list(self, arg):
        """List the working directory contents."""
        try:
            print(os.listdir(self.working_dir))
        except Exception as e:
            print(f"Exception: {e}")
        
    def do_exit(self, arg):
        """Exits the application."""
        return True  # Stop running commands

    # Callback for invalid commands
    def default(self, arg):
        """Handles non registered commands."""
        cmd_splitted = arg.split(maxsplit=1)
        if cmd_splitted[0] in self.variables:
            if callable(self.variables[cmd_splitted[0]]):
                print(self.variables[cmd_splitted[0]](self, cmd_splitted[1] if len(cmd_splitted) > 1 else None))
            else:
                print(self.variables[cmd_splitted[0]])
        else:
            print("Unknown command: ", cmd_splitted[0])
