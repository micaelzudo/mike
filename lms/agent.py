import lms.defaults as defaults
from lms.core import store
from lms.autogen import (get_agent as get_autogen_agent,
                         get_human_agent as get_autogen_human_agent,
                         get_local_executor_agent as get_autogen_local_executor_agent,
                         register_llm_tool)

class lms_agent():
    def __init__(self,
                 name:              str = "agent",
                 model:             str = defaults.general_llm,
                 system_message:    str = "You are a helpful AI assistant",
                 host:              str = "127.0.0.1",
                 max_replies:       int = None,
                 framework:         str = ""):
        self.name = name
        self.model = model
        self.system_message = system_message
        self.host = host
        self.max_replies = max_replies
        self.framework = framework
    
class lms_autogen_agent(lms_agent):
    def __init__(self,
                 name:              str = "agent",
                 model:             str = defaults.general_llm,
                 system_message:    str = "You are a helpful AI assistant",
                 host:              str = "127.0.0.1",
                 max_replies:       int = None):
        super().__init__(name=name, model=model, system_message=system_message, host=host, max_replies=max_replies, framework = "autogen")
        self.agent_instance = get_autogen_agent(name=name, model=model, system_message=system_message, host=host, max_replies=max_replies)
        self.human_agent_instance = get_autogen_human_agent()
    def query(self, message: str) -> str:
        self.human_agent_instance.send(message=message,
            recipient = self.agent_instance,
            request_reply = True,
            silent = True)
        return self.human_agent_instance.last_message(agent = self.agent_instance)["content"]
    def clear_history(self, recipient = None, n_messages_to_keep: int = None):
        self.human_agent_instance.clear_history(recipient = self.agent_instance,
            nr_messages_to_preserve = n_messages_to_keep if n_messages_to_keep else 0)
        self.agent_instance.clear_history(recipient = self.human_agent_instance,
            nr_messages_to_preserve = n_messages_to_keep if n_messages_to_keep else 0)
    
class lms_autogen_coder(lms_autogen_agent):
    def __init__(self,
                 name:              str = "coder",
                 model:             str = defaults.coder_llm,
                 system_message:    str = "You are a helpful AI software developer",
                 host:              str = "127.0.0.1",
                 max_replies:       int = None):
        super().__init__(name=name, model=model, system_message=system_message, host=host, max_replies=max_replies)
    
class lms_autogen_tooler(lms_autogen_agent):
    def __init__(self,
                 name:              str = "tooler",
                 model:             str = defaults.tooler_llm,
                 system_message:    str = "You are a helpful AI assistant",
                 host:              str = "127.0.0.1",
                 max_replies:       int = 1,
                 working_folder:    str = store["working_folder"]):
        super().__init__(name=name, model=model, system_message=system_message, host=host, max_replies=max_replies)
        from lms.agent_tools import tool_dict
        self.executor_instance = get_autogen_local_executor_agent(working_folder)
        for function_name in tool_dict:
            register_llm_tool(tooler = self.agent_instance, executor = self.executor_instance,
                              function = tool_dict[function_name][0], function_name = function_name,
                              function_desc = tool_dict[function_name][1])
    def query(self, message: str) -> str:
        chat_result = self.executor_instance.initiate_chat(
            self.agent_instance, message=message, silent=True)
        return chat_result.summary
