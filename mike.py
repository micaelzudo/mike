import os
from lms_ag import get_coder_agent, get_tooler_agent, get_local_executor_agent, get_human_agent, register_llm_tool, tooler_llm, coder_llm
from lms_stdout import lms_stdout

std_out_lms = lms_stdout()

working_folder = "/mike/working"

developer = get_coder_agent("llama3.2")
tooler = get_tooler_agent("llama3.2")
executor = get_local_executor_agent(working_folder)
human = get_human_agent()
    
def list_files() -> str:
    return os.listdir(working_folder);

def read_file(file_name: str) -> str:
    with open(working_folder + "/" + file_name, "r") as file:
        return file.read()
    
def write_file(file_name: str, file_contents: str) -> bool:
    file = open(working_folder + "/" + file_name, "w")
    file.write(file_contents)
    file.close()
    return True;

def run_python_file(file_name: str) -> str:
    std_out_lms.mark_data_as_read()
    with open(working_folder + "/" + file_name) as file:
        try:
            exec(file.read())
        except Exception as e:
            print("Exception: " + str(e))
    execution_output = std_out_lms.get_unread_data()
    write_file(file_name + ".txt", execution_output)
    return execution_output

def create_python_file(file_name: str) -> str:
    print("Creating python file " + file_name)
    developer.clear_history()
    prompt_message = "DEV: Tell me your Python algorithm. Type 'exit' when the code is right"
    chat_message = str("You will write Python code. "
    "Give only the code. Do not use code block delimiters. Do not give explanation. "
    "The code algorithm is: ")
    file_execution_output = ""
    done = False
    while not done:
        print(prompt_message)
        python_file_chat_result = human.initiate_chat(developer, clear_history=False, message=chat_message + input("DEV> "))
        write_file(file_name, python_file_chat_result.summary)
        cmd = input("Hit Enter to run the script, or type 'exit' to finish: ")
        if cmd != "exit":
            while True:
                print("Running the python file " + file_name + "... ")
                file_execution_output = run_python_file(file_name)
                cmd = input("Hit Enter to give feedback and send the script execution output to the developer, "
                            "type 'run' to execute the script again, or type 'exit' to finish: ")
                if cmd == "exit":
                    done = True
                    break
                elif cmd == "run":
                    continue
                else:
                    chat_message = "The code was executed and the output was:\n```output\n" + file_execution_output + "\n```\n"
                    prompt_message = str("DEV: Give feedback about the last code, or hit enter to submit just the execution output. "
                    "Say 'exit' when the code is right: ")
                    break
        else:
            done = True
    return file_execution_output;

register_llm_tool(tooler, executor, list_files, "list_files",
                  "A function that lists the files in the working folder")
register_llm_tool(tooler, executor, read_file, "read_file",
                  "A function that reads the contents of a file in the working folder")
register_llm_tool(tooler, executor, write_file, "write_file",
                  "A function that writes content to a file in the working folder")
register_llm_tool(tooler, executor, run_python_file, "run_python_file",
                  "A function that runs python files in the working folder")
register_llm_tool(tooler, executor, create_python_file, "create_python_file",
                  "A function that creates a python file in the working folder")
            
print("Milu's Code Generator v0.1b\n")
print("Models:\tCoder: " + coder_llm() + "\tTooler: " + tooler_llm())
print("Say 'exit' to quit\n")

# user_input_list = ["give me code that fetches the EUR price in USD from the last week, and plot it into a graph"]
user_input_list = ["create the python file \"hi.py\""]
# user_input_list = ["run the python file \"helo.py\"", "run the python file \"by.py\""]
# user_input_list = []

app_running = True
while app_running:
    print("\nEnter your commands one per line, followed by an empty line")
    # user_input_list = []
    user_input = ""
    while len(user_input) != 0 or len(user_input_list) == 0:
        user_input = input(">>> ")
        if len(user_input) != 0:
            user_input_list.append(user_input)
        if user_input == "exit":
            break

    for user_input_line in user_input_list:
        if user_input_line != 'exit':
            chat_result = executor.initiate_chat(tooler, message=user_input_line, silent=False)
            print(chat_result.summary)
        else:
            print("\nQuitting... Bye")
            app_running = False
    
    user_input_list = []#remove
