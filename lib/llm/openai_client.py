import os

from openai import OpenAI


class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def talk(self,
             agent_index: int,
             game_setting: str,
             game_info: str,
             talkHistory: str
             ) -> str:
        messages = _create_talk_messages(agent_index,
                                         game_setting,
                                         game_info,
                                         talkHistory)
        print(messages)
        return
        response = self.client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo-1106",  # TODO: 後でconfigから取得するようにする
            temperature=0.5
        )
        return response.choices[0].message.content

    def vote(self):
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": "投票する"}],
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "vote",
                        "description": "最も怪しい人の番号を返す",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "agentIdx": {
                                    "type": "int",
                                    "description": "最も人狼っぽいと思う人の番号",
                                },
                            },
                            "required": ["agentIdx"],
                        },
                    },
                }
            ],
            tool_choice="none",
            model="gpt-3.5-turbo-1106",  # TODO: 後でconfigから取得するようにする
            temperature=0.5
        )
        return


def _create_talk_messages(agent_index, game_setting, game_info, talkHistory):
    messages = [
        {
            "role": "system",
            "content": "あなたは人狼ゲームの参加者です。以下の条件をもとに続きの会話を考えてください。"
        },
        {
            "role": "user",
            "content": game_setting
                    + "\n"
                    + game_info
                    + "\n現在の会話\n"
                    + talkHistory
                    + "\n" 
                    + f"Agent[{agent_index}](あなた):",
        },
    ]
    return messages
