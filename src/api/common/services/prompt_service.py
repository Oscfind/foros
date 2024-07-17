import json
import logging

from sqlalchemy import Engine
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from src.domain.entities.models import FewShotExample, LLMModel, Prompt


class PromptService:
    _logger: logging.Logger
    _database_engine: Engine

    def __init__(
        self, logger: logging.Logger, sql_engine: Engine = None
    ) -> None:
        self._logger = logger
        self._database_engine = sql_engine

    def load_sys_prompt_from_file(self, json_name: str) -> Prompt:
        self._logger.debug(
            "load_sys_prompt input {json_name}",
            extra={"json_name": str(json_name)},
        )
        path = json_name
        with open(path, encoding="utf-8") as json_file:
            prompt_json = json.load(json_file)

        prompt = Prompt(**prompt_json)
        prompt.llm_model = LLMModel(name=prompt_json["deployment_name"], description="")
        prompt.few_shot_examples = [
            FewShotExample(
                user_input=example["userInput"],
                chatbot_response=example["chatbotResponse"],
            )  # type: ignore
            for example in prompt_json["examples"]
        ]

        self._logger.debug(
            "load_sys_prompt output {prompt}",
            extra={
                "prompt": str(prompt),
            },
        )
        return prompt

    def load_sys_prompt_from_db(self, prompt_name: str) -> Prompt:
        self._logger.debug(
            "load_sys_prompt input {json_name}",
            extra={"name": str(prompt_name)},
        )

        with Session(self._database_engine) as session:
            prompt: Prompt = session.exec(  # type: ignore
                select(Prompt)
                .where(Prompt.name == prompt_name)
                .options(
                    selectinload(Prompt.llm_model),  # type: ignore
                    selectinload(Prompt.few_shot_examples),  # type: ignore
                )
            ).one()

        self._logger.debug(
            "load_sys_prompt output {prompt}",
            extra={
                "prompt": str(prompt),  # type: ignore
            },
        )

        return prompt  # type: ignore