import cmd
import asyncio
import os
from types import MethodType, FunctionType
from collections.abc import Callable
import lms.defaults as defaults
from lms.io import lms_stdout
from lms.agent import lms_autogen_coder as lms_coder, get_code_blocks
# from lms.utils import data_dumper
# from lms.core import store

async def a_input(prompt: str = "8> ") -> str:
    return await asyncio.to_thread(input, f'{prompt}')

class project_file():
    def __init__(self, name: str = "", relative_path: str = "", absolute_path: str = ""):
        self.name = name
        self.relative_path = relative_path
        self.absolute_path = absolute_path

class project():
    def __init__(self, name: str, config_file_path: str):
        self.name = name
        self.config_file_path = config_file_path

class terminalizer(cmd.Cmd):
    
    def __init__(self, working_dir: str = defaults.working_dir, prompt: str = "8> ",
                 intro: str = "Lulu Terminal.   Type help or ? to list commands.\n", variables: dict = {}):
        super().__init__()
        self.stdout = lms_stdout()
        self.variables = variables
        # self.set_builtin_variables()
        self.do_cd(working_dir)
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

    def do_cd(self, arg):
        """Sets the working directory."""
        try:
            os.chdir(arg)
            self.working_dir = os.getcwd()
        except Exception as e:
            print(f"Exception: {e}")
    
    def do_pwd(self, arg):
        """Shows the working directory path."""
        print(self.working_dir)
    
    def do_ls(self, arg):
        """List the working directory contents."""
        try:
            print(os.listdir(self.working_dir))
        except Exception as e:
            print(f"Exception: {e}")
    
    def do_proj(self, arg: str = ""):
        """Initializes a project for development."""
        if not "project" in self.variables:
            self.variables["project"] = {}
            if not "name" in self.variables["project"]:
                self.variables["project"]["name"] = arg
            if not "files" in self.variables["project"]:
                self.variables["project"]["files"] = []

    def add_file_to_project(self, file_name: str):
        file_path = os.path.abspath(file_name)
        if not file_path in self.variables["project"]["files"]:
            self.variables["project"]["files"].append(file_path)
    
    def do_add(self, arg):
        """Add a file or folder to the current project."""
        self.do_project()
        if os.path.isfile(arg):
            self.add_file_to_project(arg)
        elif os.path.isdir(arg):
            for file_name in os.listdir(arg):
                self.do_add(arg + "/" + file_name)
    
    def do_agent(self, arg = ""):
        """Set the agent to be used in the terminal."""
        self.agent = lms_coder(model=(arg if arg else (os.environ["LLM_CODER"] if os.environ["LLM_CODER"] else defaults.coder_llm)))

    def do_brief(self, arg: str = ""):
        """Read or summarize the project files."""
        if "project" in self.variables:
            self.variables["project"]["summary"] = ""
            if "files" in self.variables["project"]:
                for file_path in self.variables["project"]["files"]:
                    self.variables["project"]["summary"] += "``` " + file_path + "\n" + open(file_path).read() + "\n```\n\n"

    def do_dev(self, arg: str = ""):
        """Generate code with the AI."""
        # dev = lms_coder()
        self.do_brief()
        prompt_message = "Give instructions to the AI: "
        user_input = input(prompt_message)
        dev_input = (arg + "\n") if arg else ""
        try:
            if self.variables["project"]["summary"]:
                dev_input += "\nThe project already has these files:\n\n" + self.variables["project"]["summary"]
        except:
            pass
        while user_input:
            dev_input = user_input + "\n" + dev_input
            dev_output = self.agent.query(message=dev_input, silent=False)
            dev_input = ""
            self.variables["dev_output"] = dev_output
            self.variables["code_blocks"] = get_code_blocks(dev_output)
            user_input = input(prompt_message)
    
    def do_create(self, arg):
        """Create a file with help of the AI."""
        self.do_dev()
        if len(self.variables["code_blocks"]) > 1:
            code_block_index = int(input("Choose the code block to save: "))
        elif len(self.variables["code_blocks"]) == 1:
            code_block_index = 0
        else:
            return
        with open(arg, "w") as file:
            file.write(self.variables["code_blocks"][code_block_index])

    def do_runpy(self, file_name: str) -> str:
        """Runs a python file."""
        self.stdout.mark_data_as_read()
        with open(file_name) as file:
            try:
                exec(file.read())
            except Exception as e:
                print("Exception: " + str(e))
        execution_output = self.stdout.get_unread_data()
        with open(file_name + ".txt", "w") as file:
            file.write(execution_output)
        print(execution_output)
        self.variables["execution_output"] = execution_output

    def do_python(self, arg):
        """Create a python file following the python workflow."""
        # from lms.agent_tools import create_python_file
        # create_python_file(arg)
        pass
    
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
                if self.agent:
                    print(self.agent.query(message=arg))
                else:
                    print("Unknown command: ", cmd_splitted[0])

def get_agent_terminal(working_dir: str = defaults.working_dir, prompt: str = "8> ",
                 intro: str = "Lulu Terminal.   Type help or ? to list commands.\n", variables: dict = {}):
    termzr = terminalizer(working_dir=working_dir, prompt=prompt, intro=intro, variables=variables)
    # termzr.agent = lms_coder()
    # termzr.variables["code"] = "Hello World!"
    # termzr.add_method("default_callback", default_terminal_callback)
    # termzr.add_method("do_python", do_python)
    termzr.do_agent()
    return termzr