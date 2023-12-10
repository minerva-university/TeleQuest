import re
from telegram import Bot
from typing import Any
from .messages import messages


BOT_COMMANDS = ["/q", "/help"]


def find_bot_command(text: str) -> str:
    """
    This function finds the first bot command in a given text that starts with one of the allowed command prefixes.
    ---
    Parameters:
    text: str
        The text in which the bot command is to be found.
    ---
    Returns:
    str
        The first bot command found in the text, including those followed by '@botname', or an empty string if no command is found.
    """
    # Create a combined regex pattern for all commands
    command_patterns = "|".join(re.escape(command) for command in BOT_COMMANDS)
    pattern = rf"(?<![\w/.])({command_patterns})(@\w+)?\b"

    # Use re.search to find the first match
    match = re.search(pattern, text)

    # Return the matched command or an empty string if no command is found
    return match.group(0) if match else ""


def send_help_response(
    bot: Bot, chat_id: int | None, first_name: str | None, group_name: str | None
) -> Any:
    """
    This function sends the help response to the user when called from a group.
    ---
    Parameters:
    bot: telegram.Bot
        The bot object that is used to send the message.
    chat_id: int
        The id of the chat to which the message is to be sent.
    """
    return bot.send_message(
        chat_id=chat_id, text=messages["help"].format(first_name, group_name)
    )  # type: ignore
