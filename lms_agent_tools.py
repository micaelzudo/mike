import os
from lms_core import lms

def list_files() -> str:
    return os.listdir(lms["working_folder"]);

def read_file(file_name: str) -> str:
    with open(lms["working_folder"] + "/" + file_name, "r") as file:
        return file.read()
    
def write_file(file_name: str, file_contents: str) -> bool:
    file = open(lms["working_folder"] + "/" + file_name, "w")
    file.write(file_contents)
    file.close()
    return True;
    
def append_to_file(file_name: str, file_contents: str) -> bool:
    file = open(lms["working_folder"] + "/" + file_name, "a")
    file.write(file_contents)
    file.close()
    return True;

def run_python_file(file_name: str) -> str:
    lms["stdout"].mark_data_as_read()
    with open(lms["working_folder"] + "/" + file_name) as file:
        try:
            exec(file.read())
        except Exception as e:
            print("Exception: " + str(e))
    execution_output = lms["stdout"].get_unread_data()
    write_file(file_name + ".txt", execution_output)
    return execution_output

def create_python_file(file_name: str) -> str:
    from lms_agent import lms_autogen_coder
    coder = lms_autogen_coder()
    print("Running Python Script Creation Workflow... for file " + file_name)
    coder_feedback = str("You will write Python code. "
    "Give only the code. Do not use code block delimiters. Do not give explanation. "
    "The code algorithm is: ")
    python_code = ""
    file_execution_output = ""
    user_input = ""
    state = "dev"
    user_prompt = "8=> "
    while True:
        if state == "dev":
            print("Give feedback to the coder" if python_code else "Enter your Python algorithm")
            user_input = input(user_prompt)
            if user_input == "exit":
                break
            python_code = coder.query(message=coder_feedback + user_input)
            print("The code given was:\n" + python_code)
            print("Saving the python file " + file_name + "... ")
            write_file(file_name, python_code)
            coder_feedback = ""
            state = "run"
            continue
        elif state == "run":
            print("Hit Enter to run the script, or type 'dev' to give feedback to the coder, or type 'exit' to finish")
            user_input = input(user_prompt)
            if user_input == "dev":
                state = "dev"
                continue
            elif user_input == "exit":
                break
            print("Running the python file " + file_name + "... ")
            file_execution_output = run_python_file(file_name)
            state = "dbg"
            continue
        elif state == "dbg":
            print("Hit Enter to send code execution output and give feedback to the coder, or type 'run' to run the script again, or type 'exit' to finish")
            user_input = input(user_prompt)
            if user_input == "run":
                state = "run"
                continue
            elif user_input == "exit":
                break
            coder_feedback = "The code was executed and the output was:\n```output\n" + file_execution_output + "\n```\n"
            state = "dev"
            continue
    return file_name;

tool_dict = { "list_files":         [ list_files, "A function that lists the files in the working folder"],
              "read_file":          [ read_file, "A function that reads the contents of a file in the working folder"],
              "write_file":         [ write_file, "A function that writes content to a file in the working folder"],
              "append_to_file":     [ append_to_file, "A function that appends content to a file in the working folder"],
              "run_python_file":    [ run_python_file, "A function that runs python files in the working folder"],
              "create_python_file": [ create_python_file, "A function that creates a python file in the working folder"]}
