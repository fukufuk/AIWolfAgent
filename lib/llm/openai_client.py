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
        # return  # 消すとopenaiが使用できる
        response = self.client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo-1106",  # TODO: 後でconfigから取得するようにする
            temperature=0.3,
            max_tokens=100
        )
        return response.choices[0].message.content

    def vote(self,
             agent_index: int,
             game_setting: str,
             game_info: str,
             talkHistory: str
             ) -> str:  # JSON形式の文字列
        messages = _create_vote_messages(game_setting,
                                         game_info,
                                         talkHistory)
        tools = _create_vote_tools()
        print("messages", messages)
        print("tools", tools)
        # return ""  # 消すとopenaiが使用できる
        response = self.client.chat.completions.create(
            messages=messages,
            tools=tools,
            tool_choice="none",
            model="gpt-3.5-turbo-1106",  # TODO: 後でconfigから取得するようにする
            temperature=0
        )
        return response.choices[0].message.tool_calls[0].function.arguments


def _create_talk_messages(agent_index, game_setting, game_info, talkHistory):
    messages = [
        {
            "role": "system",
            "content": "あなたは人狼ゲームの参加者です。以下の条件をもとに続きの会話を50文字以内で考えてください。"
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


def _create_vote_messages(game_setting, game_info, talkHistory):
    messages = [
        {
            "role": "user",
            "content": game_setting
                    + "\n"
                    + game_info
                    + "\n現在の会話\n"
                    + talkHistory,
        },
    ]
    return messages


def _create_vote_tools():
    tools = [
        {
            "type": "function",
            "function": {
                "name": "decide_person_to_vote",
                "description": "Read the current werewolf game state and decide who to vote for",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "agentIdx": {
                            "type": "int",
                            "description": "the number of the agent who is deciding who to vote for",
                        },
                    },
                    "required": ["agentIdx"],
                },
            },
        }
    ]
    return tools
