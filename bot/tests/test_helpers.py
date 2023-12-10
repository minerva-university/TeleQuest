import unittest
from unittest.mock import AsyncMock, patch
from bot.messages import messages
from bot.helpers import find_bot_command, send_help_response


class TestBotFunctions(unittest.IsolatedAsyncioTestCase):
    async def test_find_bot_command_with_command(self) -> None:
        # Test when a valid command is present
        text_with_command = "Hello! /help@minerva_tele_quest_bot This is a test."
        result = find_bot_command(text_with_command)
        self.assertEqual(result, "/help@minerva_tele_quest_bot")

    async def test_find_bot_command_without_command(self) -> None:
        # Test when no command is present
        text_without_command = "Hello! This is a regular message."
        result = find_bot_command(text_without_command)
        self.assertEqual(result, "")

    async def test_send_help_response(self) -> None:
        # Mock the Bot object with AsyncMock
        bot_mock = AsyncMock()

        # Test sending help response
        chat_id = 123
        first_name = "John"
        group_name = "Test Group"

        # Assuming messages["help"] contains a format string
        expected_message = messages["help"].format(first_name, group_name)

        # Mock the send_message method using AsyncPatch
        with patch.object(
            bot_mock, "send_message", return_value=None
        ) as send_message_mock:
            await send_help_response(bot_mock, chat_id, first_name, group_name)

        # Assert that send_message was called with the expected parameters
        send_message_mock.assert_awaited_once_with(
            chat_id=chat_id, text=expected_message
        )
