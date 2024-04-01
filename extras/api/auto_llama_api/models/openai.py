from typing import Literal, Union, Optional
from enum import Enum
from .base import BaseSchema
from pydantic import Field

from auto_llama import ChatMessage


class OpenAIResponseFormat(BaseSchema):
    """Specifies the response format of the LLM"""

    type: Literal["text", "json"]


class OpenAITool(BaseSchema):
    """Specifies a tool available to the LLM"""

    class Function(BaseSchema):
        """Specifies a function tool"""

        description: str = None
        name: str
        parameters: dict = None

    type: Literal["function"]
    function: "OpenAITool.Function"


class OpenAIToolCall(BaseSchema):
    class Function(BaseSchema):
        name: str
        arguments: str

    id: str
    type: Literal["function"]
    function: "OpenAIToolCall.Function"


class OpenAICompletionBase(BaseSchema):
    """OpenAI completion parameters"""

    model: str = Field(default="gpt-3.5-turbo", description="**UNSUPORTED**")
    frequency_penalty: float | None = Field(default=None, description="**UNSUPORTED**")
    logit_bias: dict[int, float] | None = Field(default=None, description="**UNSUPORTED**")
    logprobs: bool | None = Field(default=None, description="**UNSUPORTED**")
    top_logprobs: int | None = Field(default=None, description="**UNSUPORTED**")
    max_tokens: int | None = None
    n: int = Field(default=1, description="**UNSUPORTED**")
    presence_penalty: float = Field(default=0, description="**UNSUPORTED**")
    response_format: OpenAIResponseFormat | None = Field(default=None, description="**UNSUPORTED**")
    seed: int | None = Field(default=None, description="**UNSUPORTED**")
    stop: str | list[str] = []
    stream: bool = False
    temperature: float = Field(default=1, description="**UNSUPORTED**")
    top_p: float = Field(default=1, description="**UNSUPORTED**")
    user: str = Field(default=None, description="**UNSUPORTED**")


class OpenAICompletionResponseBase(BaseSchema):
    """OpenAI completion response"""

    class Usage(BaseSchema):
        completion_tokens: int
        prompt_tokens: int
        total_tokens: int

    id: str
    object: Literal["text_completion", "chat.completion"]
    created: int
    model: str = Field(default="gpt-3.5-turbo", description="**UNSUPORTED**")
    system_fingerprint: str = Field(default="none", description="**UNSUPORTED**")
    usage: "OpenAICompletionResponseBase.Usage" = Field(
        default=Usage(completion_tokens=0, prompt_tokens=0, total_tokens=0), description="**UNSUPORTED**"
    )


class OpenAIChoiceBase(BaseSchema):
    """OpenAI choice parameters"""

    finish_reason: Literal["stop", "length", "content_filter", "tool_calls"] | None = Field(
        default=None, description="**UNSUPORTED** (always set to 'length')"
    )
    index: int
    logprobs: Optional[dict] = Field(default=None, description="**UNSUPORTED**")


class OpenAIMessage(BaseSchema):
    """OpenAI message parameters"""

    # TODO add ToolMessage

    class Role(Enum):
        SYSTEM = "system"
        USER = "user"
        ASSISTANT = "assistant"

    class TextContent(BaseSchema):
        type: Literal["text"]
        text: str

    class ImageContent(BaseSchema):
        """**UNSUPORTED**"""

        # TODO support ImageContent

        type: Literal["image_url"]
        image_url: dict[Literal["url", "detail"], str]

    role: "OpenAIMessage.Role"
    content: str | list[Union["OpenAIMessage.TextContent"]]
    name: str | None = None

    def to_chat(self):
        """Convert to AutoLLama Chat Message"""

        return ChatMessage(role=self.role.value, message=self.content)

    @classmethod
    def from_chat(cls, msg: ChatMessage):
        """Convert from AutoLLA Chat Message to OpenAI Message"""

        return cls(role=OpenAIMessage.Role(msg.role), content=msg.message)


class OpenAIChatCompletion(OpenAICompletionBase):
    """OpenAI chat completion parameters"""

    messages: list[OpenAIMessage]
    tools: list[OpenAITool] = Field(default=[], description="**UNSUPORTED**")

    tool_choice: (
        Literal["none", "auto"] | dict[Literal["type", "function"], Literal["function"] | dict[Literal["name"], str]]
    ) = Field(default="none", description="**UNSUPORTED**")


class OpenAIChatChoice(OpenAIChoiceBase):
    """OpenAI chat choice parameters"""

    class Message(BaseSchema):
        content: str | None = None
        tool_calls: list[OpenAIToolCall] = Field(default=[], description="**UNSUPORTED**")
        role: OpenAIMessage.Role
        name: str | None = None

    message: "OpenAIChatChoice.Message"


class OpenAIChatStreamChoice(OpenAIChoiceBase):
    """OpenAI chat stream choice parameters"""

    class Message(BaseSchema):
        role: OpenAIMessage.Role
        content: str | None = None
        tool_calls: list[OpenAIToolCall] = Field(default=[], description="**UNSUPORTED**")

    delta: "OpenAIChatStreamChoice.Message"


class OpenAIChatCompletionResponse(OpenAICompletionResponseBase):
    """OpenAI chat completion response"""

    choices: list[OpenAIChatChoice | OpenAIChatStreamChoice]


class OpenAICompletion(OpenAICompletionBase):
    """OpenAI completion parameters"""

    prompt: str | list[str] | list[int] | list[list[int]]
    best_of: int = Field(default=1, description="**UNSUPORTED**")
    echo: bool = Field(default=False, description="**UNSUPORTED**")
    suffix: str | None = Field(default=None, description="**UNSUPORTED**")


class OpenAICompletionChoice(OpenAIChoiceBase):
    """OpenAI completion choice parameters (for streaming and no streaming)"""

    text: str


class OpenAICompletionResponse(OpenAICompletionResponseBase):
    """OpenAI stream completion response"""

    choices: list[OpenAICompletionChoice]
