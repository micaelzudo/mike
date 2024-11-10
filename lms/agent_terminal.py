from lms.agent import lms_autogen_coder as lms_coder
from lms.terminal import terminalizer

def get_agent_terminal():
    termzr = terminalizer()
    termzr.variables["dev"] = lambda term, args: "Hello from the dev!"
    termzr.variables["code"] = "Hello World!"
    return termzr