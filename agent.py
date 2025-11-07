
import asyncio
from datetime import datetime
from uuid import uuid4

from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatMessage,
    ChatAcknowledgement,
    TextContent,
    chat_protocol_spec,
)

from daytona import run_job_search_sandbox

agent = Agent(
    name="job-search-agent",
    seed="job-search-agent-seed-daytona",
    port=8000,
    mailbox=True,
)

protocol = Protocol(spec=chat_protocol_spec)


@protocol.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(
        sender,
        ChatAcknowledgement(timestamp=datetime.utcnow(), acknowledged_msg_id=msg.msg_id),
    )

    # Extract plain text from chat content
    text = ""
    for part in msg.content:
        if isinstance(part, TextContent):
            text += part.text
    query = (text or "").strip()

    if not query or len(query) < 3:
        await ctx.send(
            sender,
            ChatMessage(
                timestamp=datetime.utcnow(),
                msg_id=uuid4(),
                content=[
                    TextContent(
                        type="text",
                        text="Please send a job search query, e.g., 'Remote data science internship in New York'.",
                    )
                ],
            ),
        )
        return

    loop = asyncio.get_running_loop()
    try:
        _, url = await loop.run_in_executor(None, run_job_search_sandbox, query)
        reply = f"Preview URL: {url}" if url else "No results or preview unavailable."
    except Exception as e:
        reply = f"Error: {str(e)}"

    await ctx.send(
        sender,
        ChatMessage(
            timestamp=datetime.utcnow(),
            msg_id=uuid4(),
            content=[TextContent(type="text", text=reply)],
        ),
    )


@protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Acknowledged message {msg.acknowledged_msg_id} from {sender}")


agent.include(protocol, publish_manifest=True)


if __name__ == "__main__":
    agent.run()


