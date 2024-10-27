import defaults
from lms_ag import get_agent as get_autogen_agent, get_human_agent as get_autogen_human_agent

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
        self.message_history = []
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
    
class lms_autogen_tooler_agent(lms_autogen_agent):
    def __init__(self,
                 name:              str = "tooler",
                 model:             str = defaults.general_llm,
                 system_message:    str = "You are a helpful AI assistant",
                 host:              str = "127.0.0.1"):
        super().__init__(name=name, model=model, system_message=system_message, host=host, framework = "autogen")
        self.agent_instance = get_autogen_agent(name=name, model=model, system_message=system_message, host=host)
        self.message_history = []
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
