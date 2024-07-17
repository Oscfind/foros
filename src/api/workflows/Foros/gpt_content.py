from src.api.common.services.openai_service import OpenAIService
from src.api.common.services.prompt_service import PromptService
import json, logging


class GptContent:
    _openai_service: OpenAIService
    _prompt_service: PromptService

    def __init__(self, openai_service: OpenAIService, prompt_service: PromptService):
        self._openai_service = openai_service
        self._prompt_service = prompt_service

    def get_foros_content(self, content:str):
        logging.info(f"get_schema_content input question={content}") 
        prompt = self._prompt_service.load_sys_prompt_from_file(
            json_name='src/api/workflows/Foros/prompts/prompt.json'
        )
        output = self._openai_service.call_api(
            prompt=prompt,
            user_msg=content
        )
        return json.loads(output)