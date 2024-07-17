from src.api.common.services.openai_service import OpenAIService
from src.api.common.services.prompt_service import PromptService
from src.api.workflows.FAQs.gpt_faqs import GptFAQs


class FAQsWorkflow:
    _openai_service: GptFAQs
    
    def __init__(self,
        openai_service: OpenAIService, 
        prompt_service: PromptService
    ) -> None:
        self._openai_service = GptFAQs(openai_service, prompt_service)

    def execute(self, request: str) -> dict: 
        return self._openai_service.get_faqs_azure(str(request), get_prompt_from_file=True)