import os

from openai import OpenAI


class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.model = "gpt-3.5-turbo-1106"

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
            model=self.model,
            temperature=0.5,
            max_tokens=80
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
            tool_choice={"type": "function", "function": {"name": "decide_person_to_vote"}},
            model=self.model,
            temperature=0
        )
        return response.choices[0].message.tool_calls[0].function.arguments

    def divine(self,
               index: int,
               game_setting: str,
               game_info: str,
               role_suspicion: str,
               talkHistory: str) -> str:  # JSON形式の文字列
        messages = _create_divine_messages(game_setting,
                                           game_info,
                                           role_suspicion,
                                           talkHistory)
        tools = _create_divine_tools(index)
        response = self.client.chat.completions.create(
            messages=messages,
            tools=tools,
            tool_choice={"type": "function", "function": {"name": "decide_person_to_divine"}},
            model=self.model,
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
            tool_choice={"type": "function", "function": {"name": "decide_person_to_attack"}},
            model=self.model,
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
            "content": "あなたは人狼ゲームの参加者です。以下の条件をもとに次に続く発言を50文字以内で考えてください。"
                    + "発言は会話を深めるようにクリエイティブさを意識してください。"
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
                            "type": "integer",
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


def _create_divine_tools(index: int):
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
                            "type": "integer",
                            "description": f"the number of the agent which you should divine. choose from {[i for i in range(1, 6) if i != index]}",
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
                            "type": "integer",
                            "description": "the number of the agent who is deciding who to attack",
                        },
                    },
                    "required": ["agentIdx"],
                },
            },
        }
    ]
    return tools
