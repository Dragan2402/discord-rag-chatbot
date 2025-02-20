import logging
import os
from interactions import (
    Client,
    Intents,
    OptionType,
    SlashContext,
    listen,
    slash_command,
    slash_option,
)

from helpers.env import EnvironmentKeys

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

bot = Client(intents=Intents.ALL)


@listen()
async def on_ready():
    logging.info("Ready")


@slash_command(
    name="ask",
    description="Ask anything about Serbian History, expect about Battle of Maritsa :)",
)
@slash_option(
    name="question",
    description="Question text",
    required=True,
    opt_type=OptionType.STRING,
)
async def get_response(ctx: SlashContext, question: str):
    await ctx.defer()
    try:
        logging.info(f"Received input: {question}")
        await ctx.send("This is echo: " + question)
    except Exception as e:
        logging.error(f"Error: {e}")
        await ctx.send("Unexpected error occurred, try again later")


bot.start(os.getenv(EnvironmentKeys.DISCORD_BOT_ID.value))
