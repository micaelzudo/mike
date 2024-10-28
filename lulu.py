# from lms_ag import get_coder_agent, get_tooler_agent, get_local_executor_agent, get_human_agent, register_llm_tool
from lms_agent import lms_autogen_agent, lms_autogen_tooler, lms_autogen_coder
from lms_agent_tools import working_folder, lms_stdout as std_out_lms
from lms_stdout import lms_stdout

std_out_lms = lms_stdout()

working_folder = "/mike/working"

# developer = lms_autogen_agent()
tooler = lms_autogen_tooler()
# executor = get_local_executor_agent(working_folder)
# human = get_human_agent()

# register_llm_tool(tooler, executor, list_files, "list_files",
#                   "A function that lists the files in the working folder")
# register_llm_tool(tooler, executor, read_file, "read_file",
#                   "A function that reads the contents of a file in the working folder")
# register_llm_tool(tooler, executor, write_file, "write_file",
#                   "A function that writes content to a file in the working folder")
# register_llm_tool(tooler, executor, run_python_file, "run_python_file",
#                   "A function that runs python files in the working folder")
# register_llm_tool(tooler, executor, create_python_file, "create_python_file",
#                   "A function that creates a python file in the working folder")
            
print("Milu's Code Generator v0.1b\n")
print("Say 'exit' to quit\n")

# user_input_list = ["give me code that fetches the EUR price in USD from the last week, and plot it into a graph"]
# user_input_list = ["create the python file \"hi.py\""]
# user_input_list = ["run the python file \"helo.py\"", "run the python file \"by.py\""]
# user_input_list = []

app_running = True
while app_running:
    print("\nEnter your commands one per line, followed by an empty line")
    user_input_list = []
    user_input = ""
    while len(user_input) != 0 or len(user_input_list) == 0:
        user_input = input(">>> ")
        if len(user_input) != 0:
            user_input_list.append(user_input)
        # if user_input == "exit":
            break

    for user_input_line in user_input_list:
        if user_input_line != 'exit':
            print("\n" + tooler.query(message=user_input_line))
        else:
            print("\nQuitting... Bye")
            app_running = False
    
    # user_input_list = []#remove
