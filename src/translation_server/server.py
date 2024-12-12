# /// script
# dependencies = [
#   "mcp"
# ]
# ///
from mcp.shared.exceptions import McpError
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    TextContent,
    Tool,
    Prompt,
    INVALID_PARAMS,
    INTERNAL_ERROR,
)
from translation_server.utils import get_translate_prompts

MAX_TOKENS_PER_CHUNK = 500  # if text is more than this many tokens, we'll break it up into discrete chunks to translate one chunk at a time

translation_flow = Prompt(
    name="translation_flow",
    description="Translate a text from one language to another",
    arguments=[
        PromptArgument(
            name="source_language",
            description="The language of the text to be translated",
            required=True,
        ),
        PromptArgument(
            name="target_language",
            description="The language to translate the text to",
            required=True,
        ),
        PromptArgument(
            name="text",
            description="The text to be translated",
            required=True,
        ),
        PromptArgument(
            name="country",
            description="The country of the text to be translated",
            required=True,
        ),
    ],
)


async def serve() -> None:
    server = Server("mcp-translator")

    @server.list_prompts()
    async def handle_list_prompts() -> list[Prompt]:
        return [translation_flow]

    @server.get_prompt()
    async def handle_get_prompt(
        name: str, arguments: dict[str, str] | None
    ) -> GetPromptResult:
        if name == translation_flow.name:
            if arguments is None:
                return INVALID_PARAMS
            source_language = arguments.get("source_language")
            target_language = arguments.get("target_language")
            text = arguments.get("text")
            country = arguments.get("country")
            if (
                source_language is None
                or target_language is None
                or text is None
                or country is None
            ):
                return INVALID_PARAMS

            prompts = get_translate_prompts(
                source_lang=source_language,
                target_lang=target_language,
                source_text=text,
                country=country,
                max_tokens=MAX_TOKENS_PER_CHUNK,
            )

            messages = []
            for prompt in prompts:
                messages.append(
                    PromptMessage(
                        role="user",
                        content=TextContent(
                            type="text", text=f"{prompt[0]}\n{prompt[1]}".strip()
                        ),
                    )
                )

            return GetPromptResult(
                description="Translate the text",
                messages=messages,
            )

        return GetPromptResult(
            description="undefine prompt",
            messages=[
                PromptMessage(
                    content=TextContent(
                        text="undefine prompt",
                    ),
                )
            ],
        )

    options = server.create_initialization_options()
    async with stdio_server() as (reader, writer):
        await server.run(reader, writer, options)
