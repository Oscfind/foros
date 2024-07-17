from datetime import datetime
from typing import List, Optional
from sqlmodel import (
    TIMESTAMP,
    Column,
    Field,  # type: ignore
    MetaData,
    Relationship,
    SQLModel,
    text,
)


schema_name = "preparador"
metadata = MetaData(schema=schema_name)

class Prompt(SQLModel, table=True):
    __tablename__: str = "prompt"  # type: ignore
    prompt_id: Optional[int] = Field(default=None, primary_key=True)
    category: str = Field(default=None, max_length=300)
    name: str = Field(default=None, max_length=100)
    version: int
    description: str = Field(default=None, max_length=300)
    system_message: str
    llm_model_id: int = Field(default=None, foreign_key="llm_model.llm_model_id")
    llm_model: "LLMModel" = Relationship(back_populates="prompts")
    max_response_length: int
    temperature: float
    top_probabilities: float
    stop_sequences: str
    frequency_penalty: float
    presence_penalty: float
    few_shot_examples: List["FewShotExample"] = Relationship(back_populates="prompt")
    stream: bool
    is_json: Optional[bool]
    created_by: str = Field(max_length=50)
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    updated_by: str = Field(max_length=50)
    updated_at: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    is_active: bool
    is_default: bool
    metadata = metadata


class LLMModel(SQLModel, table=True):
    __tablename__: str = "llm_model"  # type: ignore
    llm_model_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)
    description: str = Field(max_length=300)
    prompts: List["Prompt"] = Relationship(back_populates="llm_model")
    metadata = metadata


class FewShotExample(SQLModel, table=True):
    __tablename__: str = "few_shot_example"  # type: ignore
    few_shot_example_id: Optional[int] = Field(default=None, primary_key=True)
    prompt_id: int = Field(foreign_key="prompt.prompt_id")
    prompt: "Prompt" = Relationship(back_populates="few_shot_examples")
    user_input: str
    chatbot_response: str
    metadata = metadata