from autogen import ConversableAgent
from autogen.coding import LocalCommandLineCodeExecutor
from autogen.coding.base import CodeExtractor

import lms.defaults as defaults

def get_agent(name:             str = "agent",
              model:            str = defaults.general_llm,
              system_message:   str = "You are a helpful AI assistant",
              host:             str = "127.0.0.1",
              max_replies:      int = None) -> ConversableAgent:
    return ConversableAgent(
        name=name,
        system_message=system_message,
        max_consecutive_auto_reply=max_replies,
        human_input_mode="NEVER",
        llm_config={"config_list": [
        {
            "model": model,
            "api_type": "ollama",
            "client_host": host
        }
    ]},
    )

def get_coder_agent(name:           str = "coder",
                    model:          str = defaults.coder_llm,
                    system_message: str = "You are a helpful AI code writer",
                    host:           str = "127.0.0.1",
                    max_replies:    int = None) -> ConversableAgent:
    return get_agent(name = name, model = model, system_message = system_message, host = host, max_replies = max_replies)

def get_tooler_agent(name:              str = "tooler",
                     model:             str = defaults.tooler_llm,
                     system_message:    str = "You are a helpful AI assistant",
                     host:              str = "127.0.0.1",
                     max_replies:       int = 1) -> ConversableAgent:
    return get_agent(name = name, model = model, system_message = system_message, host = host, max_replies = max_replies)

def get_local_executor_agent(working_folder: str = defaults.working_dir, max_replies: int = 1) -> ConversableAgent:
    executor_commandline = LocalCommandLineCodeExecutor(
        timeout=10,  # Timeout for each code execution in seconds.
        work_dir=working_folder,
    )
    return ConversableAgent(
        name="executor",
        llm_config=False,
        code_execution_config={"executor": executor_commandline},  # Use the local command line code executor.
        max_consecutive_auto_reply=max_replies,
        human_input_mode="NEVER",
    )

def get_human_agent() -> ConversableAgent:
    return ConversableAgent(
        name="human",
        llm_config=False,
        code_execution_config=False,
        human_input_mode="ALWAYS",
    )

def register_llm_tool(tooler: ConversableAgent, executor: ConversableAgent,
                      function: callable, function_name: str, function_desc: str):
    tooler.register_for_llm(name=function_name, description=function_desc)(function)
    executor.register_for_execution(name=function_name)(function)

