import defaults
from lms_autogen import (get_agent as get_autogen_agent,
                         get_human_agent as get_autogen_human_agent,
                         get_local_executor_agent as get_autogen_local_executor_agent,
                         register_llm_tool)

class lms_agent():
    def __init__(self,
                 name:              str = "agent",
                 model:             str = defaults.general_llm,
                 system_message:    str = "You are a helpful AI assistant",
                 host:              str = "127.0.0.1",
                 framework:         str = ""):
        self.name = name
        self.model = model
        self.system_message = system_message
        self.host = host
        self.framework = framework
    def query(self, message: str) -> str:
        pass
    
class lms_autogen_agent(lms_agent):
    def __init__(self,
                 name:              str = "agent",
                 model:             str = defaults.general_llm,
                 system_message:    str = "You are a helpful AI assistant",
                 host:              str = "127.0.0.1"):
        super().__init__(name=name, model=model, system_message=system_message, host=host, framework = "autogen")
        self.agent_instance = get_autogen_agent(name=name, model=model, system_message=system_message, host=host)
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
                 host:              str = "127.0.0.1"):
        super().__init__(name=name, model=model, system_message=system_message, host=host)
    
class lms_autogen_tooler(lms_autogen_agent):
    def __init__(self,
                 name:              str = "tooler",
                 model:             str = defaults.tooler_llm,
                 system_message:    str = "You are a helpful AI assistant",
                 host:              str = "127.0.0.1",
                 working_folder:    str = "./working"):
        super().__init__(name=name, model=model, system_message=system_message, host=host)
        from lms_agent_tools import tool_dict
        self.executor_instance = get_autogen_local_executor_agent(working_folder)
        for function_name in tool_dict:
            register_llm_tool(self.agent_instance, self.executor_instance,
                              tool_dict[function_name][0], function_name, tool_dict[function_name][1])
    def query(self, message: str) -> str:
        self.executor_instance.send(message=message,
            recipient = self.agent_instance,
            request_reply = True,
            silent = True)
        return self.executor_instance.last_message(agent = self.agent_instance)["content"]
    # def clear_history(self, recipient = None, n_messages_to_keep: int = None):
    #     self.human_agent_instance.clear_history(recipient = self.agent_instance,
    #         nr_messages_to_preserve = n_messages_to_keep if n_messages_to_keep else 0)
    #     self.agent_instance.clear_history(recipient = self.human_agent_instance,
    #         nr_messages_to_preserve = n_messages_to_keep if n_messages_to_keep else 0)
