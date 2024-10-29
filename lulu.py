from lms_core import lms
from lms_agent import lms_autogen_agent, lms_autogen_tooler, lms_autogen_coder
from lms_stdout import lms_stdout

lms["stdout"] = lms_stdout()
lms["working_folder"] = "/mike/working"

tooler = lms_autogen_tooler()

print("Milu's Code Generator v0.1b\n")
print("Say 'exit' to quit\n")

app_running = True
while app_running:
    # print("\nEnter your commands one per line, followed by an empty line")
    print("\nEnter your command")
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
    