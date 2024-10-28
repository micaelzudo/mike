import os

working_folder = "./working"
lms_stdout = None

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
    lms_stdout.mark_data_as_read()
    with open(working_folder + "/" + file_name) as file:
        try:
            exec(file.read())
        except Exception as e:
            print("Exception: " + str(e))
    execution_output = lms_stdout.get_unread_data()
    write_file(file_name + ".txt", execution_output)
    return execution_output

def create_python_file(file_name: str) -> str:
    from lms_agent import lms_autogen_coder
    developer = lms_autogen_coder()
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

tool_dict = { "list_files":         [ list_files, "A function that lists the files in the working folder"],
              "read_file":          [ read_file, "A function that reads the contents of a file in the working folder"],
              "write_file":         [ write_file, "A function that writes content to a file in the working folder"],
              "run_python_file":    [ run_python_file, "A function that runs python files in the working folder"],
              "create_python_file": [ create_python_file, "A function that creates a python file in the working folder"]}
