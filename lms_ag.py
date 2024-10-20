import os

from autogen import ConversableAgent
from autogen.coding import LocalCommandLineCodeExecutor

def tooler_llm() -> str:
    try:
        return os.environ["LLM_TOOLER"]
    except:
        return "llama3.1"

def coder_llm() -> str:
    try:
        return os.environ["LLM_CODER"]
    except:
        return "llama3.1"

def get_coder_agent(model: str = "") -> ConversableAgent:
    if model:
        llm_model = model
    else:
        llm_model = coder_llm()
    return ConversableAgent(
        name="Developer",
        system_message="You are a helpful AI code writer. ",
        # max_consecutive_auto_reply=1,
        human_input_mode="NEVER",
        llm_config={"config_list": [
        {
            "model": llm_model,
            "api_type": "ollama",
            "client_host": os.environ["OLLAMA_HOST"]
        }
    ]},
    )

def get_tooler_agent(model: str = "") -> ConversableAgent:
    if model:
        llm_model = model
    else:
        llm_model = tooler_llm()
    return ConversableAgent(
        name="Tooler",
        system_message="You are a helpful AI assistant. ",
        max_consecutive_auto_reply=1,
        human_input_mode="NEVER",
        llm_config={"config_list": [
        {
            "model": llm_model,
            "api_type": "ollama",
            "client_host": os.environ["OLLAMA_HOST"]
        }
    ]},
    )

def get_local_executor_agent(working_folder: str = ".") -> ConversableAgent:
    executor_commandline = LocalCommandLineCodeExecutor(
        timeout=10,  # Timeout for each code execution in seconds.
        work_dir=working_folder,
    )
    return ConversableAgent(
        name="Executor",
        llm_config=False,
        code_execution_config={"executor": executor_commandline},  # Use the local command line code executor.
        max_consecutive_auto_reply=1,
        human_input_mode="NEVER",
    )


def get_human_agent() -> ConversableAgent:
    return ConversableAgent(
        name="Human",
        llm_config=False,
        code_execution_config=False,
        human_input_mode="ALWAYS",
    )

def register_llm_tool(tooler: ConversableAgent, executor: ConversableAgent, function: callable, function_name: str, function_desc: str):
    tooler.register_for_llm(name=function_name, description=function_desc)(function)
    executor.register_for_execution(name=function_name)(function)

