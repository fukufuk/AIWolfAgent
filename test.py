from lib.llm import openai_client

print(openai_client._create_talk_messages("game_setting", "game_info", "talkHistory"))
