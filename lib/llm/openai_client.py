import os

from openai import OpenAI


class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def talk(self,
             agent_index: int,
             game_setting: str,
             game_info: str,
             role_suspicion: str,
             talkHistory: str
             ) -> str:
        messages = _create_talk_messages(agent_index,
                                         game_setting,
                                         game_info,
                                         role_suspicion,
                                         talkHistory)
        # return  # 消すとopenaiが使用できる
        response = self.client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo-1106",  # TODO: 後でconfigから取得するようにする
            temperature=0.3,
            max_tokens=100
        )
        return response.choices[0].message.content

    def vote(self,
             game_setting: str,
             game_info: str,
             role_suspicion: str,
             talkHistory: str
             ) -> str:  # JSON形式の文字列
        messages = _create_vote_messages(game_setting,
                                         game_info,
                                         role_suspicion,
                                         talkHistory)
        tools = _create_vote_tools()
        # return ""  # 消すとopenaiが使用できる
        response = self.client.chat.completions.create(
            messages=messages,
            tools=tools,
            tool_choice="none",
            model="gpt-3.5-turbo-1106",  # TODO: 後でconfigから取得するようにする
            temperature=0
        )
        return response.choices[0].message.tool_calls[0].function.arguments

    def divine(self,
               game_setting: str,
               game_info: str,
               role_suspicion: str,
               talkHistory: str) -> str:  # JSON形式の文字列
        messages = _create_divine_messages(game_setting,
                                           game_info,
                                           role_suspicion,
                                           talkHistory)
        tools = _create_divine_tools()
        response = self.client.chat.completions.create(
            messages=messages,
            tools=tools,
            tool_choice="none",
            model="gpt-3.5-turbo-1106",  # TODO: 後でconfigから取得するようにする
            temperature=0
        )
        return response.choices[0].message.tool_calls[0].function.arguments

    def attack(self,
               game_setting: str,
               game_info: str,
               role_suspicion: str,
               talkHistory: str) -> str:  # JSON形式の文字列
        messages = _create_attack_messages(game_setting,
                                           game_info,
                                           role_suspicion,
                                           talkHistory)
        tools = _create_attack_tools()
        response = self.client.chat.completions.create(
            messages=messages,
            tools=tools,
            tool_choice="none",
            model="gpt-3.5-turbo-1106",  # TODO: 後でconfigから取得するようにする
            temperature=0
        )
        return response.choices[0].message.tool_calls[0].function.arguments


def _create_talk_messages(agent_index,
                          game_setting,
                          game_info,
                          role_suspicion,
                          talkHistory) -> list[dict]:
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
                    + "\n"
                    + role_suspicion
                    + "\n現在の会話\n"
                    + talkHistory
                    + "\n"
                    + f"Agent[{agent_index}](あなた):",
        },
    ]
    return messages


def _create_vote_messages(game_setting, game_info, role_suspicion, talkHistory):
    messages = [
        {
            "role": "user",
            "content": game_setting
                    + "\n"
                    + game_info
                    + "\n"
                    + role_suspicion
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


def _create_divine_messages(game_setting, game_info, role_suspicion, talkHistory):
    messages = [
        {
            "role": "user",
            "content": game_setting
                    + "\n"
                    + game_info
                    + "\n"
                    + role_suspicion
                    + "\n現在の会話\n"
                    + talkHistory,
        },
    ]
    return messages


def _create_divine_tools():
    tools = [
        {
            "type": "function",
            "function": {
                "name": "decide_person_to_divine",
                "description": "Read the current werewolf game state and decide who to divine",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "agentIdx": {
                            "type": "int",
                            "description": "the number of the agent who is deciding who to divine",
                        },
                    },
                    "required": ["agentIdx"],
                },
            },
        }
    ]
    return tools


def _create_attack_messages(game_setting, game_info, role_suspicion, talkHistory):
    messages = [
        {
            "role": "user",
            "content": game_setting
                    + "\n"
                    + game_info
                    + "\n"
                    + role_suspicion
                    + "\n現在の会話\n"
                    + talkHistory,
        },
    ]
    return messages


def _create_attack_tools():
    tools = [
        {
            "type": "function",
            "function": {
                "name": "decide_person_to_attack",
                "description": "Read the current werewolf game state and decide who to attack",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "agentIdx": {
                            "type": "int",
                            "description": "the number of the agent who is deciding who to attack",
                        },
                    },
                    "required": ["agentIdx"],
                },
            },
        }
    ]
    return tools
