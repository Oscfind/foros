from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
import os

class LLM:
    def __init__(self):
        self.model_dict = {
            "openai": {
                "gpt-4-turbo": "gpt-4-turbo", 
                "gpt-4-turbo-preview": "gpt-4-turbo-preview",
                "gpt-3.5-turbo-0125": "gpt-3.5-turbo-0125",
            },
            "anthropic": {
                "claude-3-opus-20240229": "claude-3-opus-20240229",
                "claude-3-sonnet-20240229": "claude-3-sonnet-20240229",
                "claude-3-haiku-20240307": "claude-3-haiku-20240307",
            }
        }

    def chat_openai(self, model_name = "gpt-35-turbo-dev", max_tokens = None):
        #TODO: In the future we can filter by mode but for now the chat models from langchain
        llm = ChatOpenAI(openai_api_key = "c29595dd045545f3b8ae04c999faca04", model_name = model_name, max_tokens = max_tokens)
        return llm

    def chat_anthropic(self, model_name = "claude-3-sonnet-20240229", max_tokens = None):
        llm = ChatAnthropic(anthropic_api_key = os.environ.get("CLAUDE_API_KEY"), model_name = model_name, max_tokens = max_tokens)
        return llm

    def get_llm(self, provider, model_name = None, max_tokens = 4096):
        if provider == "openai":
            if model_name != None:
                return self.chat_openai(model_name = model_name, max_tokens = max_tokens)
            else:
                return self.chat_openai() 
        elif provider == "anthropic":
            if model_name != None:
                return self.chat_anthropic(model_name = model_name, max_tokens= max_tokens)
            else:
                return self.chat_anthropic()

    def get_available_models(self):
        return self.model_dict

    def copy(self):
        return copy.deepcopy(self)