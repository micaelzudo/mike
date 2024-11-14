from lms.agent import lms_autogen_coder as lms_coder
from lms.terminal import terminalizer
import lms.defaults as defaults

# class terminal_agent():
#     def __init__(self):
#         self.agent = lms_coder(name="agent")
    # def __call__(self, termzr, arg: str) -> str:
        # return self.query(message)
        # pass

def default_terminal_callback(self, arg):
    # print("Hello from the default terminal callback! You typed: ", arg)
    print(self.agent.query(message=arg))

def do_dev(self, arg):
    from lms.agent_tools import create_python_file
    create_python_file(arg)

def get_agent_terminal(working_dir: str = defaults.working_dir, prompt: str = "8> ",
                 intro: str = "Lulu Terminal.   Type help or ? to list commands.\n", variables: dict = {}):
    termzr = terminalizer(working_dir=working_dir, prompt=prompt, intro=intro, variables=variables)
    termzr.agent = lms_coder()
    # termzr.variables["code"] = "Hello World!"
    termzr.add_method("default_callback", default_terminal_callback)
    termzr.add_method("do_dev", do_dev)
    return termzr