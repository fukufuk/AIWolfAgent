import json
import os

from lib.logger import build_logger
from openai import OpenAI

LOGGER = build_logger(__name__)


class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.model = "gpt-4-1106-preview"  # "gpt-3.5-turbo-0125"  #

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
            max_tokens=100
        )
        return response.choices[0].message.content

    def vote(self,
             game_setting: str,
             game_info: str,
             role_suspicion: str,
            #  talkHistory: str
             ) -> str:  # JSON形式の文字列
        messages = _create_vote_messages(game_setting,
                                         game_info,
                                         role_suspicion,)
                                        #  talkHistory)
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
        response = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
        LOGGER.info(f"vote response: {response}")
        return json.dumps({"agentIdx": response["agentIdx"]})

    def divine(self,
               index: int,
               game_setting: str,
               game_info: str,
               role_suspicion: str) -> str:  # JSON形式の文字列
        messages = _create_divine_messages(game_setting,
                                           game_info,
                                           role_suspicion)
        tools = _create_divine_tools(index)
        response = self.client.chat.completions.create(
            messages=messages,
            tools=tools,
            tool_choice={"type": "function", "function": {"name": "decide_person_to_divine"}},
            model=self.model,
            temperature=0
        )
        divine_res = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
        if divine_res["agentIdx"] == index:
            return None
        return response.choices[0].message.tool_calls[0].function.arguments
        response = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
        LOGGER.info(f"divine response: {response}")
        return json.dumps({"agentIdx": response["agentIdx"]})

    def attack(self,
               game_setting: str,
               game_info: str,
               role_suspicion: str) -> str:  # JSON形式の文字列
        messages = _create_attack_messages(game_setting,
                                           game_info,
                                           role_suspicion)
        tools = _create_attack_tools()
        response = self.client.chat.completions.create(
            messages=messages,
            tools=tools,
            tool_choice={"type": "function", "function": {"name": "decide_person_to_attack"}},
            model=self.model,
            temperature=0
        )
        return response.choices[0].message.tool_calls[0].function.arguments
        response = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
        LOGGER.info(f"attack response: {response}")
        return json.dumps({"agentIdx": response["agentIdx"]})


def _create_talk_messages(agent_index,
                          game_setting,
                          game_info,
                          role_suspicion,
                          talkHistory) -> list[dict]:
    messages = [
        {
            "role": "system",
            "content": "あなたは人狼ゲームの参加者です。以下の条件をもとに次に続く発言を50文字以内で考えてください。"
                    + "発言はゲームを自分の陣営の勝利に導くように会話を深めながら積極性を発揮してください。"
                    + "占い師は占い結果を積極的に伝えることが重要です。また、人狼や狂人は村人や占い師になりすましてください。"
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
                    + f"Agent[0{agent_index}](あなた):",
        },
    ]
    return messages


def _create_vote_messages(game_setting, game_info, role_suspicion,):
                        #   talkHistory):
    messages = [
        {
            "role": "user",
            "content": game_setting
                    + "\n"
                    + game_info
                    + "\n"
                    + role_suspicion
                    # + "\n現在の会話\n"
                    # + talkHistory,
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
                            "description": "Agent[01]~[05]の中で最も怪しい（人狼と疑われる）人物の番号を選択してください。例: 1",
                        },
                    },
                    "required": ["agentIdx"],
                },
            },
        }
    ]
    return tools


def _create_divine_messages(game_setting, game_info, role_suspicion):
    messages = [
        {
            "role": "user",
            "content": game_setting
                    + "\n"
                    + game_info
                    + "\n"
                    + role_suspicion,
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
                            "description": f"この夜に占うべきプレイヤーの番号。{[i for i in range(1, 6) if i != index]}から選んでください。人狼だと疑わしい人を選択し、もし該当する人がいない場合ランダムに選択してください。例: 1",
                        },
                    },
                    "required": ["agentIdx"],
                },
            },
        }
    ]
    return tools


def _create_attack_messages(game_setting, game_info, role_suspicion):
    messages = [
        {
            "role": "user",
            "content": game_setting
                    + "\n"
                    + game_info
                    + "\n"
                    + role_suspicion
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
                            "description": "自分以外で占い師と思われるプレイヤーの番号を記述してください。例: 1",
                        },
                    },
                    "required": ["agentIdx"],
                },
            },
        }
    ]
    return tools
