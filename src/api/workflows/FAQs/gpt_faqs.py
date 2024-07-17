from src.api.common.services.openai_service import OpenAIService
from src.api.common.services.prompt_service import PromptService
import logging, os, json


class GptFAQs:
    _openai_service: OpenAIService
    _prompt_service: PromptService

    def __init__(self, openai_service: OpenAIService, prompt_service: PromptService):
        self._openai_service = openai_service
        self._prompt_service = prompt_service

    def get_faqs_azure(self, content:str, get_prompt_from_file: bool = False):
        logging.info(f"get_schema_content input question={content}") 
        prompt_name = "prompt"
        if get_prompt_from_file:
            prompt = self._prompt_service.load_sys_prompt_from_file(
                os.path.join(
                    os.sep.join(__file__.split(os.sep)[:-1]),
                    "prompts",
                    f"{prompt_name}.json",
                )
            )
        else:
            prompt = self._prompt_service.load_sys_prompt_from_db(prompt_name)
        output = self._openai_service.call_api(
            prompt=prompt,
            user_msg=content
        )
        return json.loads(output)